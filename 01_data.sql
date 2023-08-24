--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: CONSTANTS; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public."CONSTANTS" ("ID", "NAME", "VALUE") FROM stdin;
\.


--
-- Data for Name: EVENT_TYPE; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public."EVENT_TYPE" ("ID", "NAME", "DESCRIPTION") FROM stdin;
2	comitee_event	Vorstand
3	chalet	Chalet
1	scout_event	Pfadfinder
\.


--
-- Data for Name: USER; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public."USER" ("ID", "USERNAME", "HASHED_PASSWORD", "HASH_SALT", "IS_ACTIVE", "CREATED_AT", "UPDATED_AT", "FIRST_NAME", "LAST_NAME", "PROFILE_PIC_URL") FROM stdin;
19	superuserprod	2fe449faa7c8ba9c214c4dbcb97fa54b0008ae6ff52cc4c68102492bb6b6722fd4c54c468ed8f2b60504b85fc82941156768d56e8a5718dd2f3aefd55300068b	ef2400ca6188788fda4ca49dccdec976	\N	2023-07-24 17:46:31.557744+00	\N	\N	\N	\N
32	newTester	0eee9d51f7a12475d4c8da52d1d01e118909574a319766878af038aa1e4e8b7af0d6ca0766ee185ec06cfe3e9ac6cb33e8025aeb14113953de07273718afa7f8	5737add26e2b3d941929a1d61b6c8541	\N	2023-08-13 23:29:24.581014+00	2023-08-13 23:30:39.6328+00	newer	Tester	\N
27	kenji	72bb38df6a1ea4e67bdccb2f888ef7781737f17f6b379083a094891c17598b0900f611fbb7df656aaa504f7e5d098e9e97b0d5e0e77bfca9c236aa7c20660050	a1abcd9b9f7ea8d5d0174727b85fdd52	\N	2023-08-06 16:45:13.201131+00	2023-08-14 12:41:52.805898+00	Gilles	Silvestri	\N
15	user7	be3434ea8daa6e0df58019382d0cab5d5340802ba626f5bad111b9a0e03755d08b019976e5566a1a8932d80ee3276b8bcb1879a4d8c06f3f43b55bca647ca039	d4cbdfe989ebe9edde452872801c1c17	\N	2023-07-16 16:26:39.054232+00	\N	Ethan	Johnson	\N
20	superusertest	4f11335e231541da29a0a2b7966a22ddb86538188bd6ac37b12df012627b8c72befce62446eb10e55b7e479f88337823b991f106b0a5f5616c22fd22412e95f7	d4d4f064a877944d44651c5dc2d235d8	\N	2023-08-03 22:53:40.741402+00	\N	\N	\N	\N
17	user9	63565670353fdf46dd48cefe31f731a1ffed5df6c06891e2d8612133dba7cb3f01db80c5935b15b61036bb50bc02e74a7914be74e1e7fedb9c4fcd4cd34d3abd	c4e0a722ef771fd75a1a587cc7c13dae	\N	2023-07-16 16:26:41.659602+00	\N	Benjamin	Jones	\N
13	user5	00eb9c413d349b7b4ca926ce1379be16b2db02cee41e10ac4d4cfc6e519c4f2cb0b24579816b75465bb61519870cc11fd471367adf4a1298e4442d49e73e1dae	1f0baa477ba8f11f5e76a88bcecb83cc	\N	2023-07-16 16:26:36.252244+00	\N	Noah	Martinez	\N
16	user8	051f32d55dccbd700f92ad45df0568bc12d08758938ffb5f1d0114cd577c9dc1572ba710bcb220cc357a48bd13709836bb49c881a7f9b130013854e4ada09927	f87001eece476e8f04eca8c587d2e992	\N	2023-07-16 16:26:40.270392+00	\N	Ava	Williams	\N
18	user10	7848024943351b8e24f88d62d56d74b1633dbed3359faf94f58e6ae29f1f5329d2e16cc4163bd7f4d00c369c5881699d72db3323b17de063876d141170814ee8	f84fcfcffb3ab9e53d065bf051944bd7	\N	2023-07-16 16:26:43.073617+00	2023-08-06 16:41:58.305721+00	Emily	Brown	\N
2	superuser	cef94ed2955e5ed97cfef2afac25506bc8ad8a85725ea001e87db0bc7c71c0eae8e4d903d0def8b17b1679b303fb5c4ba5108070bdee614b5ad72f3a0452ea1a	e9adc51d55fbba9976a578b23cd1a5e7	\N	2023-06-26 17:28:18.476914+00	2023-08-06 11:12:31.513739+00	Super Test	User	\N
30	guy	d80ab772900483ad3f8c0097aa03715e975bfd6e5e70abb83e38b0dab6833eabd55ea21becf53633191b8906c96d192572de78d6aa5998ae1220907d2dd5d876	87d8254a6a28a277221e9b90633f1de8	\N	2023-08-06 17:46:30.346172+00	\N	Guy	Schubert	\N
9	user1	4420f8b964e325405313483978a5e659429368b4542507e671907c3f2e4680b9e89732d6252a7b4e3c1c4001dece22125493009b80132bec315822b7f0b06ee5	9d243dc46bb02d7c139b0871e214cbb3	\N	2023-07-16 16:26:29.6547+00	2023-08-07 17:07:48.06252+00	Jameson	Wilson	\N
29	mara	a4f0b9b354449d19bfc0f4224e94d2e7706d2b2737b6b9cfa67c6a7aae1d008bad69489e1f7d53c15f1e6059816e3d939259b14def360ff56515e5d4d83b36cd	a67a45a2e70a20f4f2f0f62515cac8c5	\N	2023-08-06 17:44:13.938289+00	2023-08-08 21:48:47.724246+00	Mara	Martinso	\N
31	sedam	5fc437f44e308a1b6101f78a881eccd2cf8b8df5f06540bd19a8b481dfb6a25fa25ca3430e4a994ed31684c6b7ad822d3fb00db0bc805570a69c660f7256d1ab	fcfea0a9cdea4658371bd74a9e259cea	\N	2023-08-09 22:24:25.68222+00	2023-08-10 12:55:51.85199+00	Daniel	Soares	\N
\.


--
-- Data for Name: EVENT; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public."EVENT" ("ID", "CREATED_BY", "EVENT_TYPE", "TITLE", "DESCRIPTION", "START_DATE", "END_DATE", "CREATED_AT", "UPDATED_AT") FROM stdin;
93	2	2	Silver Wedding Anniversary	Celebration of 25 years of marriage with family and friends.	2023-08-25 12:00:00+00	2023-08-25 22:00:00+00	2023-07-16 16:18:39.073864+00	2023-08-13 20:34:59.915035+00
188	2	1	Scouts' Star Night	An evening to observe the sky in the night.	2023-08-24 19:00:00+00	2023-08-25 01:00:00+00	2023-08-14 22:57:38.529269+00	2023-08-14 23:14:49.45774+00
75	2	1	Scouts' Campfire Night	An evening of storytelling, music, and camaraderie around the campfire.	2023-09-15 16:00:00+00	2023-09-15 19:00:00+00	2023-07-16 16:16:55.109312+00	\N
76	2	1	Nature Photography Hike	Hike through our local trails and learn some nature photography techniques.	2023-10-01 07:00:00+00	2023-10-01 12:00:00+00	2023-07-16 16:16:57.362434+00	\N
77	2	1	Scout Cooking Challenge	Test your outdoor cooking skills in this friendly and delicious competition.	2023-10-15 07:00:00+00	2023-10-15 16:00:00+00	2023-07-16 16:17:03.027913+00	\N
79	2	1	Night Sky Observation	Learn about constellations and the night sky in this evening event.	2023-11-15 17:00:00+00	2023-11-15 20:00:00+00	2023-07-16 16:17:15.098544+00	\N
80	2	1	Scouts Orienteering Challenge	Hone your navigation skills in this orienteering challenge through the local forest.	2023-12-01 08:00:00+00	2023-12-01 17:00:00+00	2023-07-16 16:17:21.277576+00	\N
81	2	1	Scouts Year-end Party	A fun and friendly gathering to celebrate the achievements of the past year and look forward to the next.	2023-12-15 17:00:00+00	2023-12-15 20:00:00+00	2023-07-16 16:17:27.187913+00	\N
86	2	2	Committee Team Building Activity	A day of fun and bonding activities to enhance the camaraderie among committee members.	2023-10-05 12:00:00+00	2023-10-05 14:00:00+00	2023-07-16 16:17:57.007505+00	\N
87	2	2	Meeting with Scout Leaders	A session to discuss upcoming scout events, achievements, and improvements needed.	2023-10-20 12:00:00+00	2023-10-20 14:00:00+00	2023-07-16 16:18:03.20952+00	\N
88	2	2	Committee Training Workshop	A workshop to enhance our skills and knowledge in managing our group more effectively.	2023-11-05 13:00:00+00	2023-11-05 15:00:00+00	2023-07-16 16:18:09.29061+00	\N
89	2	2	Annual Budget Planning	A crucial meeting to plan and discuss the budget allocation for the next year.	2023-11-20 13:00:00+00	2023-11-20 15:00:00+00	2023-07-16 16:18:15.185465+00	\N
90	2	2	Committee Year-end Review	Meeting to review and reflect on our performance this year and plan for the coming year.	2023-12-05 13:00:00+00	2023-12-05 15:00:00+00	2023-07-16 16:18:21.199151+00	\N
91	2	2	Committee Appreciation Gathering	A time for us to celebrate our successes and recognize the hard work of everyone in the committee.	2023-12-20 13:00:00+00	2023-12-20 15:00:00+00	2023-07-16 16:18:27.055627+00	\N
95	2	3	Local Artists Exhibition	A showcase of works by local artists in the community.	2023-09-30 12:00:00+00	2023-09-30 20:00:00+00	2023-07-16 16:18:51.370874+00	\N
97	2	3	Civic Engagement Workshop	A workshop aimed at promoting civic engagement and community involvement.	2023-10-25 08:00:00+00	2023-10-25 16:00:00+00	2023-07-16 16:19:03.135855+00	\N
98	2	3	Christmas Eve Charity Gala	A charity event to raise funds for local charities on Christmas Eve.	2023-12-24 18:00:00+00	2023-12-25 00:00:00+00	2023-07-16 16:19:09.004136+00	\N
99	2	3	New Year's Eve Celebration	A celebration to ring in the New Year with music, food, and fireworks.	2023-12-31 19:00:00+00	2024-01-01 01:00:00+00	2023-07-16 16:19:15.179934+00	\N
100	2	3	Book Club Annual Meeting	The annual meeting of a local book club with guest speakers and book signings.	2024-01-10 12:00:00+00	2024-01-10 16:00:00+00	2023-07-16 16:19:20.983474+00	\N
101	2	3	Local Business Networking Event	An event for local business owners to network and share best practices.	2024-01-25 17:00:00+00	2024-01-25 21:00:00+00	2023-07-16 16:19:27.252284+00	\N
\.


--
-- Data for Name: ROLE; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public."ROLE" ("ID", "NAME") FROM stdin;
1	admin
2	super
3	chefleitung
4	chef
5	chefassistent
6	committee
7	chalet
\.


--
-- Data for Name: ROLE_EVENT_TYPE; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public."ROLE_EVENT_TYPE" ("ROLE_ID", "EVENT_TYPE_ID", "CAN_EDIT", "CAN_SEE", "CAN_ADD") FROM stdin;
1	1	t	t	t
1	2	t	t	t
1	3	t	t	t
2	1	t	t	t
2	2	t	t	t
2	3	t	t	t
3	2	f	t	f
6	2	t	t	t
3	3	f	t	f
5	3	f	t	f
6	3	f	t	f
7	3	f	t	f
3	1	t	t	t
4	1	t	t	t
5	1	f	t	f
6	1	f	t	f
\.


--
-- Data for Name: USER_ROLE; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public."USER_ROLE" ("USER_ID", "ROLE_ID") FROM stdin;
2	1
2	2
19	2
19	1
20	2
27	2
27	1
27	7
27	3
31	2
29	5
30	6
30	7
32	2
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: dbtest_mtpe_user
--

COPY public.alembic_version (version_num) FROM stdin;
a04ac3f7b505
\.


--
-- Name: CONSTANTS_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: dbtest_mtpe_user
--

SELECT pg_catalog.setval('public."CONSTANTS_ID_seq"', 1, false);


--
-- Name: EVENT_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: dbtest_mtpe_user
--

SELECT pg_catalog.setval('public."EVENT_ID_seq"', 190, true);


--
-- Name: EVENT_TYPE_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: dbtest_mtpe_user
--

SELECT pg_catalog.setval('public."EVENT_TYPE_ID_seq"', 5, true);


--
-- Name: ROLE_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: dbtest_mtpe_user
--

SELECT pg_catalog.setval('public."ROLE_ID_seq"', 7, true);


--
-- Name: USER_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: dbtest_mtpe_user
--

SELECT pg_catalog.setval('public."USER_ID_seq"', 32, true);


--
-- PostgreSQL database dump complete
--

