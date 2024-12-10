import smtplib
import ssl
from email.message import EmailMessage
from decouple import config


class forgetPasswordMail():

    def __init__(self) -> None:
        self.email = config('MAIL_USER')
        self.password = config('MAIL_PASSWORD')
        self.server = config('MAIL_SERVER')
        self.port = config('MAIL_PORT')

    def send(self, **args):

        mail = EmailMessage()
        mail['Subject'] = args['subject']
        mail['From'] = self.email
        mail['To'] = args['to']
        mail.set_content(f'''
            <!doctype html>
                <html lang="en-US">

                <head>
                    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
                    <title>Recuperar Contraseña</title>
                    <meta name="description" content="Reset Password Email Template.">
                    <style type="text/css">
                        a:hover
                    </style>
                </head>

                <body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
                    <!--100% body table-->
                    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
                        style="@import  url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,700|Open+Sans:300,400,600,700); font-family: 'Open Sans', sans-serif;">
                        <tr>
                            <td>
                                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                                    align="center" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="height:80px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                        <td style="text-align:center;">
                                            #
                                          </a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="height:20px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table width="95%" border="0" align="center" cellpadding="0" cellspacing="0"
                                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                                <tr>
                                                    <td style="height:40px;">&nbsp;</td>
                                                </tr>
                                                <tr>
                                                    <td style="padding:0 35px;">
                                                    <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:30px;font-family:'Rubik',sans-serif;">Hola!, { args['name'] }</h1>
                                                        <h3 style="color:#1e1e2d; font-weight:500; margin: 5px;font-size:16px;font-family:'Rubik',sans-serif;">Su código de recuperación de contraseña es:</h3>

                                                        <h1 style="color:#1e1e2d; font-weight:500; margin:5;font-size: 30px;font-family:'Rubik',sans-serif;"><b>{ args['code'] }</b></h1>
                                                        <span
                                                            style="display:inline-block; vertical-align:middle; margin:29px 0 26px; border-bottom:1px solid #cecece; width:100px;"></span>
                                                        <p style="color:#455056; font-size:15px;line-height:24px; margin:0;">
                                                            Copyright © Maxcodex </p>
                                                        <p style="color:#455056; font-size:9px;line-height:24px; margin:5px;">
                                                            Este código tiene una duración máxima de 30 minutos. </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="height:40px;">&nbsp;</td>
                                                </tr>
                                            </table>
                                        </td>
                                    <tr>
                                        <td style="height:20px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                        <td style="text-align:center;">
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="height:80px;">&nbsp;</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <!--/100% body table-->
                </body>

                </html>
            ''', subtype='html')

        try:
            smtp = smtplib.SMTP(self.server, self.port)
            smtp.login(self.email, self.password)
            smtp.send_message(mail)

            return True

        except Exception as message_error:
            print(message_error)
            return False
