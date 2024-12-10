import io
import os
import random
import string
import tempfile
import shutil
import numpy as np
from pypdf import PdfReader, PdfWriter
from fastapi.responses import FileResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from PIL import Image, ImageOps
from app.helpers.aws import S3Helper as s3
from app.api.types.models import Type
from app.api.applications.models import Application
from app.resources.allows import ALLOWED_IMAGES, ALLOWED_FILES


class FileRepository:
    def __init__(self, session: Session):
        self.session = session
        self.key = self._generate_random_string(5)

    def upload_file(self, file, **args):
        type_info = Type.find(self.session, args['type_id'])
        app = Application.find(self.session, args['app_id'])

        file_name = self._construct_file_name(file_name_prefix=self.key, user_id=args['user_id'], 
                                              app_id=app.id, file_format=type_info.file_format)
        file_path = f"{type_info.name}/{file_name}"

        file_type = self._check_content_type(file.content_type, type_info.content_type)
        new_file = self._process_file(file=file, file_type=file_type, 
                                      file_name=file_name, type_info=type_info)

        url = self._upload_to_s3(app=app, file=new_file, file_path=file_path)
        self._log_operation(app=app, operation='uploaded', user_id=args['user_id'], 
                            ip=args['ip'], folder=type_info.name)

        return {'url': url, 'file_path': file_path}

    def _process_file(self, file, file_type, file_name, type_info):
        if file_type == 'image':
            return self._resize_and_clean_image(file=file, file_name=file_name, type_info=type_info)
        elif file_type == 'pdf':
            return self._process_pdf(file)

    def _resize_and_clean_image(self, file, file_name, type_info):
        try:
            pil_image = Image.open(file.file)
            pil_image = ImageOps.cover(pil_image, (type_info.width, type_info.height))
            pil_image = ImageOps.exif_transpose(pil_image)

            in_mem_file = io.BytesIO()
            pil_image.save(in_mem_file, format=type_info.file_format)
            in_mem_file.seek(0)
            return in_mem_file

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    def _process_pdf(self, file):
        try:
            input_pdf_stream = io.BytesIO(file.file.read())
            output_pdf_stream = io.BytesIO()

            self._remove_pdf_metadata(input_pdf_stream, output_pdf_stream)
            output_pdf_stream.seek(0)
            return output_pdf_stream

        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    def _remove_pdf_metadata(self, input_pdf_stream, output_pdf_stream):
        reader = PdfReader(input_pdf_stream)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({})
        writer.write(output_pdf_stream)

    def remove_file(self, **args):
        app = Application.find(self.session, args['app_id'])

        self._log_operation(app=app, operation='removed', user_id=args['user_id'], 
                            ip=args['ip'], folder=args['file_path'])

        if s3(app).remove(args['file_path']):
            return {'message': f"The file {args['file_path']} has been removed"}

        raise HTTPException(status_code=400, detail=f"The file {args['file_path']} does not exist")

    def _generate_random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def _check_content_type(self, file_content_type, expected_content_type):
        if file_content_type == expected_content_type:
            if file_content_type in ALLOWED_IMAGES:
                return "image"
            elif file_content_type in ALLOWED_FILES:
                return "pdf"
        raise HTTPException(status_code=400, detail="The file you are trying to upload does not match the allowed format")

    def _construct_file_name(self, file_name_prefix, user_id, app_id, file_format):
        return f"{file_name_prefix}-user-{user_id}-app-{app_id}.{file_format}"

    def _upload_to_s3(self, app, file, file_path):
        return s3(app).upload(file, file_path)

    def _log_operation(self, app, operation, user_id, ip, folder):
        s3(app).log_file(operation=operation, user_id=user_id, ip=ip, folder=folder, key=self.key)
