INSERT INTO public.users VALUES
	(1, 'Angel Narvaez', 'a.narvaez@invertropoli.com', '$2b$12$aXOCGSBPf33H8HRoYOqDKOQnCiv/vSDTPJv6JIFl/WU.sIvkXdPcW', '2024-02-19 18:52:08.024709', NULL),
	(2, 'Willians Rodriguez', 'codesarrollo@invertropoli.com', '$2b$12$CnIQ91IGFf/j1WiEPrqRnuyA2TcxuP4PjdgyRpTS./IVuD5SgzO12', '2024-02-19 18:53:41.676697', NULL);

SELECT pg_catalog.setval('public.users_id_seq', 2, true);
