--
-- PostgreSQL database dump
--

-- Dumped from database version 10.15 (Ubuntu 10.15-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.15 (Ubuntu 10.15-0ubuntu0.18.04.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: base_alertslog; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_alertslog (
    id integer NOT NULL,
    is_sent boolean NOT NULL,
    dttm_sent timestamp with time zone NOT NULL,
    alert_type character varying(2) NOT NULL,
    player_id bigint,
    tr_day_id integer,
    info text,
    payment_id integer
);


ALTER TABLE public.base_alertslog OWNER TO nikita;

--
-- Name: base_alertslog_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_alertslog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_alertslog_id_seq OWNER TO nikita;

--
-- Name: base_alertslog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_alertslog_id_seq OWNED BY public.base_alertslog.id;


--
-- Name: base_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_channel (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    code character varying(32) NOT NULL,
    token character varying(256) NOT NULL
);


ALTER TABLE public.base_channel OWNER TO postgres;

--
-- Name: base_channel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_channel_id_seq OWNER TO postgres;

--
-- Name: base_channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_channel_id_seq OWNED BY public.base_channel.id;


--
-- Name: base_grouptrainingday; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_grouptrainingday (
    id integer NOT NULL,
    date date NOT NULL,
    is_available boolean NOT NULL,
    start_time time without time zone,
    duration interval,
    group_id integer NOT NULL,
    dttm_added timestamp with time zone NOT NULL,
    dttm_deleted timestamp with time zone,
    tr_day_status character varying(1) NOT NULL,
    is_individual boolean NOT NULL
);


ALTER TABLE public.base_grouptrainingday OWNER TO postgres;

--
-- Name: base_grouptrainingday_absent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_grouptrainingday_absent (
    id integer NOT NULL,
    grouptrainingday_id integer NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.base_grouptrainingday_absent OWNER TO postgres;

--
-- Name: base_grouptrainingday_absent_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_grouptrainingday_absent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_grouptrainingday_absent_id_seq OWNER TO postgres;

--
-- Name: base_grouptrainingday_absent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_grouptrainingday_absent_id_seq OWNED BY public.base_grouptrainingday_absent.id;


--
-- Name: base_grouptrainingday_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_grouptrainingday_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_grouptrainingday_id_seq OWNER TO postgres;

--
-- Name: base_grouptrainingday_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_grouptrainingday_id_seq OWNED BY public.base_grouptrainingday.id;


--
-- Name: base_grouptrainingday_pay_visitors; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_grouptrainingday_pay_visitors (
    id integer NOT NULL,
    grouptrainingday_id integer NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.base_grouptrainingday_pay_visitors OWNER TO nikita;

--
-- Name: base_grouptrainingday_pay_visitors_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_grouptrainingday_pay_visitors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_grouptrainingday_pay_visitors_id_seq OWNER TO nikita;

--
-- Name: base_grouptrainingday_pay_visitors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_grouptrainingday_pay_visitors_id_seq OWNED BY public.base_grouptrainingday_pay_visitors.id;


--
-- Name: base_grouptrainingday_visitors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_grouptrainingday_visitors (
    id integer NOT NULL,
    grouptrainingday_id integer NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.base_grouptrainingday_visitors OWNER TO postgres;

--
-- Name: base_grouptrainingday_visitors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_grouptrainingday_visitors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_grouptrainingday_visitors_id_seq OWNER TO postgres;

--
-- Name: base_grouptrainingday_visitors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_grouptrainingday_visitors_id_seq OWNED BY public.base_grouptrainingday_visitors.id;


--
-- Name: base_payment; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_payment (
    id integer NOT NULL,
    month character varying(2) NOT NULL,
    year character varying(1) NOT NULL,
    player_id bigint,
    fact_amount integer,
    n_fact_visiting smallint,
    theory_amount integer,
    CONSTRAINT base_payment_fact_amount_check CHECK ((fact_amount >= 0)),
    CONSTRAINT base_payment_n_fact_visiting_check CHECK ((n_fact_visiting >= 0)),
    CONSTRAINT base_payment_theory_amount_check CHECK ((theory_amount >= 0))
);


ALTER TABLE public.base_payment OWNER TO nikita;

--
-- Name: base_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_payment_id_seq OWNER TO nikita;

--
-- Name: base_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_payment_id_seq OWNED BY public.base_payment.id;


--
-- Name: base_staticdata; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_staticdata (
    id integer NOT NULL,
    tarif_ind integer,
    tarif_group integer,
    tarif_arbitrary integer,
    tarif_few integer,
    tarif_section integer,
    tarif_payment_add_lesson integer DEFAULT 100,
    CONSTRAINT base_staticdata_tarif_arbitrary_check CHECK ((tarif_arbitrary >= 0)),
    CONSTRAINT base_staticdata_tarif_few_check CHECK ((tarif_few >= 0)),
    CONSTRAINT base_staticdata_tarif_group_check CHECK ((tarif_group >= 0)),
    CONSTRAINT base_staticdata_tarif_ind_check CHECK ((tarif_ind >= 0)),
    CONSTRAINT base_staticdata_tarif_section_check CHECK ((tarif_section >= 0))
);


ALTER TABLE public.base_staticdata OWNER TO nikita;

--
-- Name: base_staticdata_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_staticdata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_staticdata_id_seq OWNER TO nikita;

--
-- Name: base_staticdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_staticdata_id_seq OWNED BY public.base_staticdata.id;


--
-- Name: base_traininggroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_traininggroup (
    id integer NOT NULL,
    dttm_added timestamp with time zone NOT NULL,
    dttm_deleted timestamp with time zone,
    name character varying(32) NOT NULL,
    max_players smallint NOT NULL,
    status character varying(1) NOT NULL,
    level character varying(1) NOT NULL,
    tarif_for_one_lesson integer NOT NULL,
    available_for_additional_lessons boolean NOT NULL,
    CONSTRAINT base_traininggroup_tarif_for_one_lesson_check CHECK ((tarif_for_one_lesson >= 0))
);


ALTER TABLE public.base_traininggroup OWNER TO postgres;

--
-- Name: base_traininggroup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_traininggroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_traininggroup_id_seq OWNER TO postgres;

--
-- Name: base_traininggroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_traininggroup_id_seq OWNED BY public.base_traininggroup.id;


--
-- Name: base_traininggroup_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_traininggroup_users (
    id integer NOT NULL,
    traininggroup_id integer NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.base_traininggroup_users OWNER TO postgres;

--
-- Name: base_traininggroup_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_traininggroup_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_traininggroup_user_id_seq OWNER TO postgres;

--
-- Name: base_traininggroup_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_traininggroup_user_id_seq OWNED BY public.base_traininggroup_users.id;


--
-- Name: base_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    username character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    id bigint NOT NULL,
    telegram_username character varying(64),
    first_name character varying(32),
    phone_number character varying(16),
    is_superuser boolean NOT NULL,
    is_blocked boolean NOT NULL,
    status character varying(1) NOT NULL,
    time_before_cancel interval,
    bonus_lesson smallint,
    add_info character varying(128),
    parent_id bigint
);


ALTER TABLE public.base_user OWNER TO postgres;

--
-- Name: base_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_user_groups (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.base_user_groups OWNER TO postgres;

--
-- Name: base_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_user_groups_id_seq OWNER TO postgres;

--
-- Name: base_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_user_groups_id_seq OWNED BY public.base_user_groups.id;


--
-- Name: base_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_user_user_permissions (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.base_user_user_permissions OWNER TO postgres;

--
-- Name: base_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.base_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: base_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.base_user_user_permissions_id_seq OWNED BY public.base_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: base_alertslog id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_alertslog ALTER COLUMN id SET DEFAULT nextval('public.base_alertslog_id_seq'::regclass);


--
-- Name: base_channel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_channel ALTER COLUMN id SET DEFAULT nextval('public.base_channel_id_seq'::regclass);


--
-- Name: base_grouptrainingday id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday ALTER COLUMN id SET DEFAULT nextval('public.base_grouptrainingday_id_seq'::regclass);


--
-- Name: base_grouptrainingday_absent id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_absent ALTER COLUMN id SET DEFAULT nextval('public.base_grouptrainingday_absent_id_seq'::regclass);


--
-- Name: base_grouptrainingday_pay_visitors id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_pay_visitors ALTER COLUMN id SET DEFAULT nextval('public.base_grouptrainingday_pay_visitors_id_seq'::regclass);


--
-- Name: base_grouptrainingday_visitors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors ALTER COLUMN id SET DEFAULT nextval('public.base_grouptrainingday_visitors_id_seq'::regclass);


--
-- Name: base_payment id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_payment ALTER COLUMN id SET DEFAULT nextval('public.base_payment_id_seq'::regclass);


--
-- Name: base_staticdata id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_staticdata ALTER COLUMN id SET DEFAULT nextval('public.base_staticdata_id_seq'::regclass);


--
-- Name: base_traininggroup id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_traininggroup ALTER COLUMN id SET DEFAULT nextval('public.base_traininggroup_id_seq'::regclass);


--
-- Name: base_traininggroup_users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_traininggroup_users ALTER COLUMN id SET DEFAULT nextval('public.base_traininggroup_user_id_seq'::regclass);


--
-- Name: base_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_groups ALTER COLUMN id SET DEFAULT nextval('public.base_user_groups_id_seq'::regclass);


--
-- Name: base_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.base_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add user	6	add_user
17	Can change user	6	change_user
18	Can delete user	6	delete_user
19	Can add group training day	7	add_grouptrainingday
20	Can change group training day	7	change_grouptrainingday
21	Can delete group training day	7	delete_grouptrainingday
22	Can add tarif	8	add_tarif
23	Can change tarif	8	change_tarif
24	Can delete tarif	8	delete_tarif
25	Can add training group	9	add_traininggroup
26	Can change training group	9	change_traininggroup
27	Can delete training group	9	delete_traininggroup
28	Can add channel	10	add_channel
29	Can change channel	10	change_channel
30	Can delete channel	10	delete_channel
31	Can add оплата	11	add_payment
32	Can change оплата	11	change_payment
33	Can delete оплата	11	delete_payment
34	Can add Изменяемые данные	12	add_staticdata
35	Can change Изменяемые данные	12	change_staticdata
36	Can delete Изменяемые данные	12	delete_staticdata
37	Can add alerts log	13	add_alertslog
38	Can change alerts log	13	change_alertslog
39	Can delete alerts log	13	delete_alertslog
\.


--
-- Data for Name: base_alertslog; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_alertslog (id, is_sent, dttm_sent, alert_type, player_id, tr_day_id, info, payment_id) FROM stdin;
396	t	2021-01-13 02:35:28.92384+03	SP	\N	\N	\N	401
397	t	2021-01-13 02:35:59.247143+03	SP	\N	\N	\N	401
398	t	2021-01-13 02:36:29.550662+03	SP	\N	\N	\N	401
399	t	2021-01-13 02:36:59.846297+03	SP	\N	\N	\N	401
400	t	2021-01-13 02:37:30.099462+03	SP	\N	\N	\N	401
394	t	2021-01-13 02:32:39.137684+03	SP	\N	\N	\N	401
395	t	2021-01-13 02:32:44.418109+03	SP	\N	\N	\N	401
\.


--
-- Data for Name: base_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_channel (id, name, username, code, token) FROM stdin;
1	TestTennisTulaBot	TestTennisTulaBot	tennis	1224814504:AAFsEymeCAygTKKx3NiBLStffgAon0bx2hM
2	admin tennis	TestAdminTennisTulaBot	admin	1159521643:AAGNeanoIy6y5_W62c2P6kgdDsx73aPrfIw
\.


--
-- Data for Name: base_grouptrainingday; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_grouptrainingday (id, date, is_available, start_time, duration, group_id, dttm_added, dttm_deleted, tr_day_status, is_individual) FROM stdin;
1	2020-07-14	t	09:30:00	01:30:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
222	2020-07-16	t	16:30:00	01:30:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
223	2020-07-23	t	16:30:00	01:30:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
333	2020-08-05	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
351	2020-08-06	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
332	2020-08-01	t	18:00:00	01:00:00	1797	2020-08-18 12:24:44.267179+03	\N	M	f
353	2020-08-20	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
335	2020-08-19	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
396	2020-08-19	t	12:30:00	01:00:00	1797	2020-08-18 12:24:44.267179+03	\N	M	f
398	2020-08-20	t	13:30:00	01:30:00	1803	2020-08-18 12:24:44.267179+03	\N	M	f
394	2020-08-19	t	14:00:00	02:00:00	1803	2020-08-18 12:24:44.267179+03	\N	M	f
382	2020-08-19	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
399	2020-08-20	t	11:30:00	02:00:00	1803	2020-08-18 12:24:44.267179+03	\N	M	f
401	2020-08-20	t	08:00:00	01:00:00	1803	2020-08-18 12:24:44.267179+03	\N	M	f
297	2020-08-13	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
300	2020-09-03	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
301	2020-09-10	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
302	2020-09-17	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
303	2020-09-24	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
304	2020-10-01	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
323	2020-07-30	t	16:30:00	01:30:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
925	2020-12-04	t	12:00:00	01:00:00	1	2020-12-08 00:18:54.548546+03	\N	M	f
251	2020-10-31	t	12:00:00	01:00:00	1796	2020-10-13 16:50:47.610889+03	\N	M	f
252	2020-11-07	t	12:00:00	01:00:00	1796	2020-10-13 16:50:47.610951+03	\N	M	f
253	2020-11-14	t	12:00:00	01:00:00	1796	2020-10-13 16:50:47.610988+03	\N	M	f
296	2020-08-06	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
352	2020-08-13	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
325	2020-08-13	t	17:00:00	01:00:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
326	2020-08-20	t	16:30:00	01:30:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
327	2020-08-27	t	16:30:00	01:30:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
299	2020-08-27	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
355	2020-09-03	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
298	2020-08-20	t	18:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
334	2020-08-12	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
336	2020-08-26	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
338	2020-09-09	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
339	2020-09-16	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
340	2020-09-23	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
341	2020-09-30	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
356	2020-09-10	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
357	2020-09-17	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
358	2020-09-24	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
360	2020-08-06	t	11:00:00	01:00:00	1797	2020-08-18 12:24:44.267179+03	\N	M	f
337	2020-09-02	t	09:30:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
342	2020-09-11	t	18:00:00	01:00:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
343	2020-09-18	t	18:00:00	01:00:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
344	2020-09-25	t	18:00:00	01:00:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
345	2020-10-02	t	18:00:00	01:00:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
346	2020-10-09	t	18:00:00	01:00:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
365	2020-08-30	t	10:30:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
366	2020-09-06	t	10:30:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
367	2020-09-13	t	10:30:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
368	2020-09-20	t	10:30:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
369	2020-09-27	t	10:30:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
397	2020-08-19	t	17:00:00	01:00:00	1797	2020-08-18 12:24:44.267179+03	\N	M	f
400	2020-08-20	t	19:00:00	01:00:00	1797	2020-08-18 12:24:44.267179+03	\N	M	f
324	2020-08-06	t	16:30:00	01:30:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
362	2020-08-09	t	13:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
361	2020-08-06	t	13:00:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
370	2020-08-09	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
372	2020-08-23	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
373	2020-08-30	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
374	2020-09-06	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
375	2020-09-13	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
376	2020-09-20	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
377	2020-09-27	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
378	2020-10-04	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
379	2020-08-09	t	18:00:00	01:00:00	1802	2020-08-18 12:24:44.267179+03	\N	M	f
380	2020-08-09	t	10:30:00	01:30:00	1797	2020-08-18 12:24:44.267179+03	\N	M	f
381	2020-08-12	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
383	2020-08-26	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
384	2020-09-02	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
386	2020-09-16	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
387	2020-09-23	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
388	2020-09-30	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
354	2020-08-27	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
389	2020-10-07	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
390	2020-08-16	t	15:30:00	01:30:00	1803	2020-08-18 12:24:44.267179+03	\N	M	f
393	2020-08-19	t	18:00:00	02:00:00	1803	2020-08-18 12:24:44.267179+03	\N	M	f
385	2020-09-09	t	10:30:00	01:30:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
359	2020-10-01	t	10:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
363	2020-08-16	t	10:30:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
347	2020-10-16	t	18:00:00	01:00:00	1	2020-08-18 12:24:44.267179+03	\N	M	f
371	2020-08-16	t	12:00:00	01:00:00	1801	2020-08-18 12:24:44.267179+03	\N	M	f
105	2020-08-19	t	20:30:00	01:00:00	1802	2020-08-18 12:24:44.267179+03	\N	M	f
106	2020-08-26	t	17:30:00	01:00:00	1803	2020-08-20 20:12:34.374657+03	\N	M	f
254	2020-11-21	t	12:00:00	01:00:00	1796	2020-10-13 16:50:47.611019+03	\N	M	f
364	2020-08-23	t	10:30:00	01:00:00	1796	2020-08-18 12:24:44.267179+03	\N	M	f
108	2020-08-27	t	11:30:00	01:30:00	1803	2020-08-23 13:28:30.976918+03	\N	M	f
110	2020-08-25	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.587946+03	\N	M	f
111	2020-09-01	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.599824+03	\N	M	f
112	2020-09-08	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.599995+03	\N	M	f
113	2020-09-15	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600077+03	\N	M	f
114	2020-09-22	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.60014+03	\N	M	f
115	2020-09-29	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600206+03	\N	M	f
116	2020-10-06	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600269+03	\N	M	f
117	2020-10-13	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600328+03	\N	M	f
120	2020-11-03	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600508+03	\N	M	f
121	2020-11-10	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600585+03	\N	M	f
122	2020-11-17	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.60069+03	\N	M	f
123	2020-11-24	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600761+03	\N	M	f
125	2020-12-08	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600882+03	\N	M	f
126	2020-12-15	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.60094+03	\N	M	f
127	2020-12-22	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600999+03	\N	M	f
129	2021-01-05	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.601112+03	\N	M	f
130	2021-01-12	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.601172+03	\N	M	f
131	2021-01-19	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.601231+03	\N	M	f
133	2021-02-02	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.60134+03	\N	M	f
134	2021-02-09	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.601389+03	\N	M	f
135	2021-02-16	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.601434+03	\N	M	f
176	2020-09-20	t	16:30:00	02:00:00	1803	2020-09-19 13:07:33.472915+03	\N	M	t
136	2020-08-26	t	12:00:00	01:00:00	1797	2020-08-25 12:55:37.190729+03	\N	M	t
177	2020-09-27	t	16:30:00	02:00:00	1803	2020-09-19 13:07:33.55121+03	\N	M	f
255	2020-11-28	t	12:00:00	01:00:00	1796	2020-10-13 16:50:47.611048+03	\N	M	f
256	2020-12-05	t	12:00:00	01:00:00	1796	2020-10-13 16:50:47.611075+03	\N	M	f
143	2020-09-03	t	12:00:00	01:00:00	1803	2020-09-05 21:06:51.791742+03	\N	M	t
586	2020-10-03	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.308996+03	\N	M	f
587	2020-10-10	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.379358+03	\N	M	f
588	2020-10-17	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.379569+03	\N	M	f
589	2020-10-24	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.379674+03	\N	M	f
590	2020-10-31	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.379768+03	\N	M	f
591	2020-11-07	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.379844+03	\N	M	f
592	2020-11-14	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.379916+03	\N	M	f
593	2020-11-21	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.379983+03	\N	M	f
594	2020-11-28	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380061+03	\N	M	f
124	2020-12-01	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600825+03	\N	M	f
230	2020-11-30	t	18:00:00	01:00:00	1796	2020-10-13 16:49:22.881162+03	\N	M	f
178	2020-10-04	t	16:30:00	02:00:00	1803	2020-09-19 13:07:33.551305+03	\N	M	f
179	2020-10-11	t	16:30:00	02:00:00	1803	2020-09-19 13:07:33.551355+03	\N	M	f
180	2020-10-18	t	16:30:00	02:00:00	1803	2020-09-19 13:07:33.551398+03	\N	M	f
128	2020-12-29	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.601055+03	\N	M	f
132	2021-01-26	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.601289+03	\N	M	f
119	2020-10-27	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600441+03	\N	M	f
118	2020-10-20	t	13:00:00	01:00:00	1796	2020-08-25 12:22:06.600382+03	\N	M	f
225	2020-10-26	t	12:00:00	01:00:00	1796	2020-10-13 16:49:22.880875+03	\N	M	f
226	2020-11-02	t	12:00:00	01:00:00	1796	2020-10-13 16:49:22.880968+03	\N	M	f
228	2020-11-16	t	12:00:00	01:00:00	1796	2020-10-13 16:49:22.881071+03	\N	M	f
224	2020-10-19	t	12:00:00	01:00:00	1796	2020-10-13 16:49:22.872255+03	\N	M	f
250	2020-10-24	t	12:00:00	01:00:00	1796	2020-10-13 16:50:47.602585+03	\N	M	f
227	2020-11-09	t	12:00:00	01:00:00	1796	2020-10-13 16:49:22.881023+03	\N	M	f
954	2020-12-25	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.572072+03	\N	M	f
955	2021-01-01	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.57215+03	\N	M	f
956	2021-01-08	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.572195+03	\N	M	f
957	2021-01-15	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.572233+03	\N	M	f
958	2021-01-22	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.57227+03	\N	M	f
959	2021-01-29	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.572306+03	\N	M	f
960	2021-02-05	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.57234+03	\N	M	f
961	2021-02-12	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.572374+03	\N	M	f
962	2021-02-19	t	14:00:00	01:30:00	1803	2020-12-08 01:05:23.57243+03	\N	M	f
603	2021-01-30	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380707+03	\N	M	f
595	2020-12-05	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380131+03	\N	M	f
597	2020-12-19	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380297+03	\N	M	f
598	2020-12-26	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380381+03	\N	M	f
599	2021-01-02	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380435+03	\N	M	f
600	2021-01-09	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380513+03	\N	M	f
601	2021-01-16	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380574+03	\N	M	f
605	2021-02-13	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380836+03	\N	M	f
606	2021-02-20	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380889+03	\N	M	f
607	2021-02-27	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380933+03	\N	M	f
608	2021-03-06	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380976+03	\N	M	f
609	2021-03-13	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.381047+03	\N	M	f
610	2021-03-20	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.381124+03	\N	M	f
611	2021-03-27	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.381215+03	\N	M	f
596	2020-12-12	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380211+03	\N	M	f
602	2021-01-23	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380641+03	\N	M	f
604	2021-02-06	t	18:30:00	01:00:00	1	2020-10-26 22:10:33.380789+03	\N	M	f
564	2020-11-23	t	18:00:00	01:00:00	1801	2020-10-26 13:20:35.502882+03	\N	M	f
560	2020-10-26	t	18:00:00	01:00:00	1801	2020-10-26 13:20:35.325497+03	\N	M	f
561	2020-11-02	t	18:00:00	01:00:00	1801	2020-10-26 13:20:35.502658+03	\N	M	f
562	2020-11-09	t	18:00:00	01:00:00	1801	2020-10-26 13:20:35.502768+03	\N	M	f
449	2020-10-29	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936025+03	\N	M	f
450	2020-11-05	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936119+03	\N	M	f
451	2020-11-12	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936159+03	\N	M	f
452	2020-11-19	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936188+03	\N	M	f
453	2020-11-26	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936217+03	\N	M	f
455	2020-12-10	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936269+03	\N	M	f
456	2020-12-17	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936347+03	\N	M	f
457	2020-12-24	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936377+03	\N	M	f
458	2020-12-31	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936404+03	\N	M	f
459	2021-01-07	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.93643+03	\N	M	f
460	2021-01-14	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936456+03	\N	M	f
461	2021-01-21	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936482+03	\N	M	f
462	2021-01-28	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.93651+03	\N	M	f
463	2021-02-04	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936538+03	\N	M	f
464	2021-02-11	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936564+03	\N	M	f
465	2021-02-18	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936591+03	\N	M	f
466	2021-02-25	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936618+03	\N	M	f
467	2021-03-04	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936646+03	\N	M	f
468	2021-03-11	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936673+03	\N	M	f
469	2021-03-18	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.9367+03	\N	M	f
470	2021-03-25	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936725+03	\N	M	f
471	2021-04-01	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936753+03	\N	M	f
472	2021-04-08	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936779+03	\N	M	f
473	2021-04-15	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936805+03	\N	M	f
448	2020-10-22	t	13:30:00	01:00:00	1796	2020-10-22 13:03:02.921622+03	\N	M	f
484	2020-10-28	t	18:30:00	01:00:00	1803	2020-10-23 02:01:48.848627+03	\N	M	t
485	2020-11-04	t	18:30:00	01:00:00	1803	2020-10-23 02:01:48.890816+03	\N	M	f
486	2020-11-11	t	18:30:00	01:00:00	1803	2020-10-23 02:01:48.890969+03	\N	M	f
487	2020-11-18	t	18:30:00	01:00:00	1803	2020-10-23 02:01:48.891056+03	\N	M	f
952	2020-12-18	t	08:00:00	01:30:00	1803	2020-12-08 01:01:49.671144+03	\N	M	t
500	2020-12-06	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020004+03	\N	M	f
509	2021-02-07	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020968+03	\N	M	f
496	2020-11-08	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.019518+03	\N	M	f
497	2020-11-15	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.019653+03	\N	M	f
498	2020-11-22	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.019775+03	\N	M	f
501	2020-12-13	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020119+03	\N	M	f
502	2020-12-20	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020243+03	\N	M	f
503	2020-12-27	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020374+03	\N	M	f
504	2021-01-03	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020511+03	\N	M	f
505	2021-01-10	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020592+03	\N	M	f
506	2021-01-17	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020661+03	\N	M	f
507	2021-01-24	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020758+03	\N	M	f
508	2021-01-31	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.020886+03	\N	M	f
510	2021-02-14	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021038+03	\N	M	f
511	2021-02-21	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021107+03	\N	M	f
512	2021-02-28	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021192+03	\N	M	f
513	2021-03-07	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.02126+03	\N	M	f
514	2021-03-14	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021326+03	\N	M	f
494	2020-10-25	t	12:00:00	01:00:00	1	2020-10-23 21:29:02.864575+03	\N	M	f
495	2020-10-28	t	15:30:00	01:00:00	1	2020-10-23 21:29:03.019269+03	\N	M	f
563	2020-11-16	t	18:00:00	01:00:00	1801	2020-10-26 13:20:35.502832+03	\N	M	f
566	2020-12-07	t	19:00:00	01:00:00	1801	2020-10-26 13:20:35.502974+03	\N	M	f
565	2020-11-30	t	21:00:00	01:00:00	1801	2020-10-26 13:20:35.502929+03	\N	M	f
499	2020-11-29	t	23:00:00	01:00:00	1	2020-10-23 21:29:03.01989+03	\N	M	f
454	2020-12-03	t	14:10:00	01:00:00	1796	2020-10-22 13:03:02.936242+03	\N	M	f
965	2020-12-28	f	18:00:00	01:00:00	1801	2020-12-25 16:38:42.107877+03	\N	M	f
966	2021-02-05	t	13:00:00	01:00:00	6	2021-02-04 02:03:05.449513+03	\N	M	f
515	2021-03-21	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021392+03	\N	M	f
516	2021-03-28	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021498+03	\N	M	f
517	2021-04-04	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.02163+03	\N	M	f
518	2021-04-11	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021764+03	\N	M	f
519	2021-04-18	t	12:00:00	01:00:00	1	2020-10-23 21:29:03.021923+03	\N	M	f
229	2020-11-23	t	12:00:00	01:00:00	1796	2020-10-13 16:49:22.881115+03	\N	M	f
953	2020-12-18	t	14:00:00	01:30:00	1803	2020-12-08 01:05:16.003494+03	\N	M	t
963	2020-12-13	t	16:00:00	02:00:00	1803	2020-12-08 01:06:31.608455+03	\N	M	t
\.


--
-- Data for Name: base_grouptrainingday_absent; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_grouptrainingday_absent (id, grouptrainingday_id, user_id) FROM stdin;
8	323	350490234
15	299	2
19	326	350490234
20	325	350490234
21	382	340961092
3	354	638303006
4	136	340961092
5	106	350490234
9	343	350490234
11	344	350490234
12	347	350490234
13	118	638303006
17	119	2
18	224	123
22	250	4
23	227	123
24	448	2
25	448	638303006
30	494	350490234
31	495	3
32	563	1329
33	229	340961092
34	564	1329
35	594	350490234
36	124	2
37	565	1
38	230	2
39	230	638303006
41	958	350490234
43	602	22
\.


--
-- Data for Name: base_grouptrainingday_pay_visitors; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_grouptrainingday_pay_visitors (id, grouptrainingday_id, user_id) FROM stdin;
2	507	350490234
7	602	350490234
13	604	350490234
\.


--
-- Data for Name: base_grouptrainingday_visitors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_grouptrainingday_visitors (id, grouptrainingday_id, user_id) FROM stdin;
6	337	3
7	337	340961092
8	333	3
9	333	340961092
10	333	350490234
11	296	4
12	351	123
13	351	3
17	325	638303006
18	324	638303006
20	326	340961092
21	372	340961092
23	364	4
27	354	340961092
29	354	350490234
40	250	350490234
42	227	350490234
43	495	350490234
44	496	350490234
45	563	340961092
48	229	350490234
53	230	350490234
54	128	3
60	603	350490234
\.


--
-- Data for Name: base_payment; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_payment (id, month, year, player_id, fact_amount, n_fact_visiting, theory_amount) FROM stdin;
295	12	0	2	0	15	6000
287	12	0	3	0	7	2800
290	12	0	4	0	15	6000
293	12	0	123	0	15	6000
311	12	0	638303006	0	9	3600
296	12	0	3	0	7	2800
423	1	1	3	0	0	\N
212	12	0	1329	0	0	\N
283	12	0	1329	0	0	\N
318	2	0	123	0	0	\N
319	2	0	638303006	0	0	\N
397	1	1	123	0	0	\N
320	2	0	2	0	0	\N
309	12	0	340961092	0	0	\N
399	1	1	340961092	0	0	\N
26	11	0	4	0	25	10000
315	12	0	22	0	8	3200
396	1	1	4	0	0	\N
403	1	1	638303006	0	0	\N
419	1	1	1329	0	0	\N
308	12	0	4	0	15	6000
310	12	0	123	0	15	6000
14	10	0	123	0	21	8400
13	10	0	340961092	3400	9	3600
15	10	0	22	0	12	4800
304	12	0	2	0	15	6000
313	12	0	3	0	7	2800
63	12	0	350490234	0	3	4200
53	12	0	350490234	0	3	4200
281	12	0	4	0	15	6000
105	6	0	4	0	0	\N
106	6	0	1329	0	0	\N
18	10	0	350490234	4400	4	4600
107	6	0	123	0	0	\N
108	6	0	638303006	0	0	\N
284	12	0	123	0	15	6000
299	12	0	4	0	15	6000
302	12	0	123	0	15	6000
285	12	0	638303006	0	9	3600
282	12	0	340961092	0	0	\N
9	9	0	350490234	0	3	4200
22	11	0	340961092	0	1	400
24	11	0	22	0	0	\N
125	3	0	4	0	0	\N
97	9	0	1329	0	13	5200
17	10	0	4	0	21	8400
23	11	0	123	0	24	9600
12	10	0	638303006	0	13	5200
16	10	0	3	3600	9	3600
10	10	0	1	3000	3	1200
289	12	0	22	0	8	3200
292	12	0	1329	0	0	\N
43	12	0	350490234	0	3	4200
321	2	0	3	0	0	\N
322	2	0	1	0	0	\N
323	2	0	22	0	0	\N
291	12	0	340961092	0	0	\N
72	5	0	4	0	0	\N
74	5	0	1329	0	0	\N
19	11	0	1	0	1	400
25	11	0	3	0	8	3200
21	11	0	638303006	0	3	1200
38	11	0	1329	0	1	400
298	12	0	22	0	8	3200
305	12	0	3	0	7	2800
324	2	0	4	0	0	\N
325	2	0	340961092	0	0	\N
326	2	0	123	0	0	\N
300	12	0	340961092	0	0	\N
69	5	0	123	0	0	\N
307	12	0	22	0	8	3200
327	2	0	638303006	0	0	\N
76	5	0	638303006	0	0	\N
328	2	0	2	0	0	\N
329	2	0	3	0	0	\N
330	2	0	1	0	0	\N
331	2	0	22	0	0	\N
116	2	0	1329	0	0	\N
119	2	0	350490234	0	0	\N
70	5	0	2	0	0	\N
36	12	0	350490234	0	3	4200
81	12	0	350490234	0	3	4200
409	1	1	340961092	0	0	\N
400	1	1	1329	0	0	\N
416	1	1	22	0	0	\N
395	1	1	3	0	0	\N
421	1	1	638303006	0	0	\N
402	1	1	123	0	0	\N
405	1	1	3	0	0	\N
394	1	1	2	0	0	\N
413	1	1	2	0	0	\N
411	1	1	123	0	0	\N
407	1	1	22	0	0	\N
406	1	1	1	0	0	\N
404	1	1	2	0	0	\N
417	1	1	4	0	0	\N
408	1	1	4	0	0	\N
415	1	1	1	0	0	\N
410	1	1	1329	0	0	\N
418	1	1	340961092	0	0	\N
286	12	0	2	0	15	6000
110	6	0	2	0	0	\N
111	6	0	3	0	0	\N
112	6	0	1	0	0	\N
113	6	0	340961092	0	0	\N
114	6	0	22	0	0	\N
115	2	0	4	0	0	\N
117	2	0	123	0	0	\N
118	2	0	638303006	0	0	\N
120	2	0	2	0	0	\N
121	2	0	3	0	0	\N
122	2	0	1	0	0	\N
123	2	0	340961092	0	0	\N
124	2	0	22	0	0	\N
126	3	0	1329	0	0	\N
109	6	0	350490234	0	0	\N
71	5	0	3	0	0	\N
75	5	0	1	0	0	\N
73	5	0	350490234	0	0	\N
301	12	0	1329	0	0	\N
422	1	1	2	0	0	\N
412	1	1	638303006	0	0	\N
420	1	1	123	0	0	\N
398	1	1	4	0	0	\N
414	1	1	3	0	0	\N
314	12	0	1	0	1	400
288	12	0	1	0	1	400
294	12	0	638303006	0	9	3600
297	12	0	1	0	1	400
303	12	0	638303006	0	9	3600
306	12	0	1	0	1	400
20	11	0	2	0	29	11600
131	3	0	3	0	0	\N
132	3	0	1	0	0	\N
133	3	0	340961092	0	0	\N
204	4	0	22	0	0	\N
136	11	0	1329	0	3	1200
138	11	0	638303006	0	21	8400
141	11	0	1	0	4	1600
142	11	0	22	0	17	6800
27	11	0	350490234	0	7	5800
144	1	0	340961092	0	0	\N
145	1	0	1329	0	0	\N
150	1	0	3	0	0	\N
151	1	0	1	0	0	\N
139	11	0	2	0	29	11600
143	1	0	4	0	0	\N
147	1	0	638303006	0	0	\N
146	1	0	123	0	0	\N
152	1	0	22	0	0	\N
149	1	0	2	0	0	\N
148	1	0	350490234	0	0	\N
134	3	0	22	0	0	\N
127	3	0	123	0	0	\N
130	3	0	2	0	0	\N
128	3	0	638303006	0	0	\N
316	2	0	4	0	0	\N
153	3	0	4	0	0	\N
154	3	0	340961092	0	0	\N
155	3	0	1329	0	0	\N
156	3	0	123	0	0	\N
157	3	0	638303006	0	0	\N
159	3	0	2	0	0	\N
160	3	0	3	0	0	\N
161	3	0	1	0	0	\N
162	3	0	22	0	0	\N
163	3	0	4	0	0	\N
164	3	0	340961092	0	0	\N
165	3	0	1329	0	0	\N
166	3	0	123	0	0	\N
167	3	0	638303006	0	0	\N
168	3	0	2	0	0	\N
169	3	0	3	0	0	\N
170	3	0	1	0	0	\N
171	3	0	22	0	0	\N
225	9	0	1	0	13	5200
222	9	0	638303006	0	31	12400
172	3	0	4	0	0	\N
173	3	0	340961092	0	0	\N
174	3	0	1329	0	0	\N
175	3	0	123	0	0	\N
176	3	0	638303006	0	0	\N
177	3	0	2	0	0	\N
178	3	0	3	0	0	\N
179	3	0	1	0	0	\N
180	3	0	22	0	0	\N
140	11	0	3	0	8	3200
201	4	0	3	0	0	\N
181	3	0	4	0	0	\N
182	3	0	340961092	0	0	\N
183	3	0	1329	0	0	\N
184	3	0	123	0	0	\N
185	3	0	638303006	0	0	\N
186	3	0	2	0	0	\N
187	3	0	3	0	0	\N
188	3	0	1	0	0	\N
189	3	0	22	0	0	\N
129	3	0	350490234	0	0	\N
158	3	0	350490234	0	0	\N
190	6	0	4	0	0	\N
191	6	0	340961092	0	0	\N
192	6	0	1329	0	0	\N
193	6	0	123	0	0	\N
194	6	0	638303006	0	0	\N
195	6	0	2	0	0	\N
196	6	0	3	0	0	\N
197	6	0	1	0	0	\N
198	6	0	22	0	0	\N
202	4	0	4	0	0	\N
199	4	0	123	0	0	\N
206	4	0	1	0	0	\N
200	4	0	2	0	0	\N
203	4	0	638303006	0	0	\N
205	4	0	1329	0	0	\N
135	11	0	4	0	25	10000
137	11	0	123	0	24	9600
211	12	0	340961092	0	0	\N
317	2	0	340961092	0	0	\N
216	12	0	3	0	7	2800
226	9	0	22	0	18	7200
223	9	0	2	0	34	13600
11	10	0	2	0	23	9200
207	10	0	1329	0	3	1200
219	9	0	4	0	21	8400
208	4	0	340961092	0	0	\N
221	9	0	123	0	21	8400
224	9	0	3	0	4	1600
210	12	0	4	0	15	6000
228	5	0	340961092	0	0	\N
227	5	0	22	0	0	\N
213	12	0	123	0	15	6000
209	4	0	350490234	0	0	\N
453	2	1	2	0	4	1600
454	2	1	123	0	4	1600
455	2	1	22	0	4	1600
218	12	0	22	0	8	3200
220	9	0	340961092	0	1	400
424	1	1	1	0	0	\N
425	1	1	22	0	0	\N
401	1	1	350490234	0	0	\N
312	12	0	2	0	15	6000
217	12	0	1	0	1	400
215	12	0	2	0	15	6000
214	12	0	638303006	0	9	3600
456	2	1	350490234	1	2	1800
385	12	0	4	0	15	6000
388	12	0	123	0	15	6000
391	12	0	3	0	7	2800
426	1	1	4	0	0	\N
427	1	1	340961092	0	0	\N
429	1	1	123	0	0	\N
430	1	1	638303006	0	0	\N
431	1	1	2	0	0	\N
432	1	1	3	0	0	\N
386	12	0	340961092	0	0	\N
393	12	0	22	0	8	3200
433	1	1	1	0	0	\N
434	1	1	22	0	0	\N
435	1	1	4	0	0	\N
436	1	1	340961092	0	0	\N
438	1	1	123	0	0	\N
439	1	1	638303006	0	0	\N
440	1	1	2	0	0	\N
441	1	1	3	0	0	\N
442	1	1	1	0	0	\N
443	1	1	22	0	0	\N
444	1	1	4	0	0	\N
445	1	1	340961092	0	0	\N
447	1	1	123	0	0	\N
448	1	1	638303006	0	0	\N
449	1	1	2	0	0	\N
450	1	1	3	0	0	\N
451	1	1	1	0	0	\N
452	1	1	22	0	0	\N
446	1	1	1329	0	0	\N
437	1	1	1329	0	0	\N
428	1	1	1329	0	0	\N
387	12	0	1329	0	0	\N
390	12	0	2	0	15	6000
389	12	0	638303006	0	9	3600
392	12	0	1	0	1	400
\.


--
-- Data for Name: base_staticdata; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_staticdata (id, tarif_ind, tarif_group, tarif_arbitrary, tarif_few, tarif_section, tarif_payment_add_lesson) FROM stdin;
1	1400	400	600	400	4000	100
\.


--
-- Data for Name: base_traininggroup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_traininggroup (id, dttm_added, dttm_deleted, name, max_players, status, level, tarif_for_one_lesson, available_for_additional_lessons) FROM stdin;
1802	2020-08-03 23:07:27.490678+03	\N	БабаЯга	1	I	O	400	f
5	2020-08-21 11:31:29.552835+03	\N	aaaaaaaaaaaaaaadddd	1	I	O	400	f
1801	2020-08-01 14:36:58.539676+03	\N	БАНДА №3	4	G	G	400	f
1797	2020-07-31 02:34:53.959762+03	\N	ОльгаШамаева	1	I	O	400	f
8	2020-12-22 19:40:15.874197+03	\N	Детская банда	3	S	O	400	f
1796	2020-07-29 14:57:39.541131+03	\N	БАНДА №2	4	G	O	400	t
7	2020-12-22 02:37:48.638519+03	\N	ПробнаяОплата	1	G	O	400	f
1	2020-07-14 15:50:45+03	\N	БАНДА №1	5	G	O	450	t
6	2020-12-22 02:36:23.454146+03	\N	БАНДА №4	4	G	G	400	t
1803	2020-08-11 11:00:09.632172+03	\N	НикитаШамаев	1	I	O	400	f
\.


--
-- Data for Name: base_traininggroup_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_traininggroup_users (id, traininggroup_id, user_id) FROM stdin;
2	1	2
4	1	4
18	1796	22
19	1797	340961092
24	1801	1
25	1801	2
26	1801	638303006
27	1802	2
7	1803	350490234
8	1796	123
9	5	123
13	1796	2
33	1	123
37	7	1329
46	1796	1329
49	6	2
50	6	123
52	6	22
53	1	22
54	1	3
55	6	350490234
\.


--
-- Data for Name: base_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_user (password, last_login, username, last_name, email, is_staff, is_active, date_joined, id, telegram_username, first_name, phone_number, is_superuser, is_blocked, status, time_before_cancel, bonus_lesson, add_info, parent_id) FROM stdin;
	\N		Оплата		f	t	2020-10-25 17:42:03.438863+03	1329	\N	Пробная	1235123512	f	t	A	06:00:00	7	\N	\N
1	\N	3			f	t	2020-07-14 15:49:23+03	3	\N	фыв	444444	f	t	F	00:00:20	5	\N	\N
1	\N	4	asd		f	t	2020-07-14 15:50:08+03	4	\N	Кошка	789	f	t	F	00:00:00	1	\N	\N
11	\N	22			f	t	2020-07-29 14:56:20+03	22	\N	klfflkfkk	1213213214	f	t	F	00:00:23	1	\N	\N
1	\N	2	Яга		f	t	2020-07-14 15:48:58+03	2	\N	Баба	214141	f	t	F	00:00:14	2	\N	\N
1	\N	340961092	Шамаева		f	t	2020-07-31 01:15:45+03	340961092		Ольга	89611469010	f	t	W	02:00:00	0	\N	\N
1	\N	123	dddd		f	t	2020-07-29 14:55:26+03	123	\N	aaaaaaaaaaaaaaa	787978987987	f	t	F	00:00:02	1	\N	\N
pbkdf2_sha256$100000$KQ87ID09qeE9$uqHZg8uVMnjd1itviF59KxJFF04tvDPyXdBCyBzOhDA=	2021-02-03 22:46:33.454904+03	350490234	Шамаев		t	t	2020-07-15 15:13:23+03	350490234	ta2asho	Никита	89661215215	t	f	G	06:00:00	2	asd123123 sasdf	340961092
1	\N	638303006	Юрков		t	t	2020-08-02 21:26:53.659073+03	638303006	VladlenYS	Владлен	89039600906	t	t	F	03:00:00	8	\N	\N
1	\N	1	asd		f	t	2020-07-14 15:48:23+03	1	\N	Крекс	789456	f	t	F	00:02:30	2	\N	\N
\.


--
-- Data for Name: base_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: base_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
285	2020-10-22 13:01:49.505393+03	422	Группа: вторая, max_players: 6, дата тренировки 2020-10-22, время начала: 13:30:00	1	[{"added": {}}]	7	350490234
290	2020-10-23 02:03:11.996836+03	348	Группа: Первая, max_players: 6, дата тренировки 2020-10-23, время начала: 18:00:00	3		7	350490234
294	2020-10-23 22:13:19.919716+03	181	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-25, время начала: 16:30:00	2	[{"changed": {"fields": ["is_individual"]}}]	7	350490234
298	2020-10-24 13:12:15.850464+03	495	Группа: Первая, max_players: 6, дата тренировки 2020-11-01, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
302	2020-10-25 16:10:46.633048+03	18	Никита Шамаев -- 89661215215, месяц: 10	2	[]	11	350490234
306	2020-10-26 13:20:35.517199+03	560	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-10-26, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
310	2020-10-26 18:17:44.97387+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-11-02, время начала: 19:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
314	2020-10-26 18:19:33.43099+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-28, время начала: 18:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
318	2020-10-26 18:30:08.221999+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-29, время начала: 14:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
322	2020-10-26 18:34:51.838025+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-29, время начала: 16:30:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
326	2020-10-26 21:49:48.288965+03	359	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-10-01, время начала: 11:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
330	2020-10-31 01:59:10.22248+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
334	2020-11-09 20:29:29.449217+03	563	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-11-16, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
181	2020-07-15 17:53:49.243986+03	1	Первая, Group -- 400 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
182	2020-07-15 18:15:50.530932+03	1795	БабаЯга, Freelancer -- 600 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
183	2020-07-15 18:16:24.792302+03	231	Группа: БабаЯга, Freelancer -- 600 руб./час, дата тренировки 2020-07-18, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
184	2020-07-15 18:18:13.908116+03	232	Группа: БабаЯга, Freelancer -- 600 руб./час, дата тренировки 2020-07-25, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
185	2020-07-15 18:23:03.838098+03	1795	Группа Никита Шамаев, Freelancer -- 600 руб./час	2	[{"changed": {"fields": ["name"]}}]	9	350490234
186	2020-07-15 18:55:23.185217+03	232	Группа: Группа Никита Шамаев, Freelancer -- 600 руб./час, дата тренировки 2020-07-25, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
187	2020-07-16 00:21:35.544294+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["last_name", "first_name", "time_before_cancel"]}}]	6	350490234
188	2020-07-16 14:17:09.068071+03	231	Группа: Группа Никита Шамаев, Freelancer -- 600 руб./час, дата тренировки 2020-07-18, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
189	2020-07-29 14:56:09.779706+03	123	aaaaaaaaaaaaaaa dddd -- 787978987987	1	[{"added": {}}]	6	350490234
190	2020-07-29 14:57:15.039152+03	22	klfflkfkk  -- 1213213214	1	[{"added": {}}]	6	350490234
191	2020-07-29 14:57:39.870039+03	1796	вторая, Group -- 400 руб./час	1	[{"added": {}}]	9	350490234
192	2020-07-29 15:29:50.152906+03	233	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 18:01:00	1	[{"added": {}}]	7	350490234
193	2020-07-29 15:31:04.389621+03	233	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 18:01:00	3		7	350490234
194	2020-07-29 16:17:00.528714+03	242	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:01:00	1	[{"added": {}}]	7	350490234
195	2020-07-29 16:17:17.261348+03	242	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:01:00	3		7	350490234
196	2020-07-29 16:17:40.591076+03	251	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:01:00	1	[{"added": {}}]	7	350490234
197	2020-07-29 16:19:19.503063+03	251	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:01:00	3		7	350490234
198	2020-07-29 16:19:59.024645+03	260	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
199	2020-07-29 16:20:26.588889+03	260	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	3		7	350490234
200	2020-07-29 16:20:51.716646+03	269	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
201	2020-07-29 16:21:09.812155+03	269	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	3		7	350490234
202	2020-07-29 16:21:46.04546+03	278	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 13:21:41	1	[{"added": {}}]	7	350490234
203	2020-07-29 16:22:04.105621+03	278	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 13:21:41	3		7	350490234
204	2020-07-29 16:22:23.03196+03	287	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
205	2020-07-29 16:23:15.461262+03	287	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:00:00	3		7	350490234
206	2020-07-29 16:48:41.106707+03	296	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
207	2020-07-29 17:53:58.75841+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
208	2020-07-29 18:39:39.424766+03	224	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	3		7	350490234
209	2020-07-29 18:40:00.928137+03	305	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
210	2020-07-29 18:40:18.125626+03	305	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	3		7	350490234
211	2020-07-29 18:40:44.21475+03	314	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
212	2020-07-29 18:41:43.662042+03	314	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 16:30:00	3		7	350490234
213	2020-07-29 18:42:31.337441+03	323	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
214	2020-07-30 16:04:18.749461+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 15:30:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
215	2020-07-30 16:15:34.609484+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["start_time", "duration"]}}]	7	350490234
216	2020-07-30 16:17:14.653323+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
217	2020-07-30 16:17:23.714175+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
218	2020-07-30 16:44:50.555148+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
219	2020-07-30 16:44:55.749234+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
220	2020-07-30 16:45:00.746365+03	326	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-20, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
221	2020-07-30 16:45:07.73912+03	327	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-27, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
222	2020-07-30 16:55:19.605982+03	299	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-27, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
223	2020-07-31 01:43:39.182096+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
224	2020-07-31 01:46:12.001261+03	340961092	Ольга Шамаева -- 89611469010	2	[]	6	350490234
225	2020-07-31 02:05:47.114864+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
226	2020-07-31 02:06:19.159857+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
227	2020-07-31 02:06:48.045398+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
228	2020-07-31 02:07:07.260509+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
229	2020-07-31 02:07:15.461182+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
230	2020-07-31 02:34:53.963473+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
231	2020-07-31 02:36:03.600566+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-07-31, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
232	2020-07-31 02:38:59.017102+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-07-31, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
233	2020-07-31 02:41:06.144297+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-01, время начала: 18:00:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
234	2020-07-31 02:42:01.993112+03	1796	вторая, Group -- 400 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
235	2020-07-31 02:42:28.913707+03	1796	вторая, Group -- 400 руб./час	2	[]	9	350490234
236	2020-07-31 02:52:37.644662+03	296	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
237	2020-07-31 02:53:07.901936+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-01, время начала: 18:00:00	2	[]	7	350490234
238	2020-07-31 03:23:52.371782+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	6	350490234
239	2020-08-01 14:16:42.647924+03	1799	лёдИ, Freelancer -- 600 руб./час	3		9	350490234
240	2020-08-01 14:16:56.746403+03	1800	ОльгаШамаева, Freelancer -- 600 руб./час	3		9	350490234
241	2020-08-01 14:16:56.76935+03	1798	ОльгаШамаева, Freelancer -- 600 руб./час	3		9	350490234
242	2020-08-01 14:19:24.858667+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
243	2020-08-01 14:19:30.778744+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
244	2020-08-01 14:29:09.008756+03	298	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-20, время начала: 18:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
245	2020-08-01 14:36:58.548039+03	1801	третья, Group -- 400 руб./час	1	[{"added": {}}]	9	350490234
246	2020-08-01 14:37:58.885142+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	1	[{"added": {}}]	7	350490234
247	2020-08-01 14:38:39.670246+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
248	2020-08-01 14:45:26.805383+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[]	7	350490234
249	2020-08-01 14:47:53.765197+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[]	7	350490234
250	2020-08-01 14:53:20.314983+03	337	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-09-02, время начала: 09:30:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
251	2020-08-01 14:53:32.254336+03	337	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-09-02, время начала: 09:30:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
252	2020-08-01 15:12:49.483965+03	337	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-09-02, время начала: 09:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
253	2020-08-01 15:14:38.255916+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
254	2020-08-01 15:15:01.395562+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[]	7	350490234
255	2020-08-01 15:58:33.518551+03	342	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-09-11, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
256	2020-08-01 16:57:09.321836+03	1796	вторая, Group -- 400 руб./час	2	[{"changed": {"fields": ["max_players"]}}]	9	350490234
257	2020-08-01 16:57:29.912958+03	296	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
258	2020-08-01 19:28:32.851298+03	351	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 10:00:00	1	[{"added": {}}]	7	350490234
259	2020-08-01 19:29:57.865997+03	360	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-06, время начала: 11:00:00	1	[{"added": {}}]	7	350490234
260	2020-08-01 20:39:00.259924+03	351	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 10:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
261	2020-08-02 21:31:51.444546+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["status", "time_before_cancel", "bonus_lesson"]}}]	6	350490234
262	2020-08-02 21:39:14.005375+03	361	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-02, время начала: 10:30:00	1	[{"added": {}}]	7	350490234
263	2020-08-02 21:39:45.882392+03	361	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 10:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
264	2020-08-02 21:42:13.363569+03	1801	третья, Group -- 400 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
265	2020-08-03 18:58:43.864084+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
266	2020-08-03 19:59:44.974866+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
267	2020-08-03 21:14:36.411571+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
268	2020-08-03 23:02:15.821356+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
269	2020-08-03 23:06:37.335136+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
270	2020-08-03 23:06:52.082592+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[]	7	350490234
271	2020-08-03 23:07:27.749793+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
272	2020-08-04 11:49:37.725199+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
273	2020-08-04 11:50:48.875929+03	362	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-09, время начала: 13:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
274	2020-08-04 11:51:11.963504+03	361	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 13:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
275	2020-08-10 00:10:33.791354+03	370	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-09, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
276	2020-08-10 00:11:07.746082+03	379	Группа: БабаЯга, Freelancer -- 600 руб./час, дата тренировки 2020-08-09, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
277	2020-08-10 00:13:15.291502+03	380	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-09, время начала: 10:30:00	1	[{"added": {}}]	7	350490234
278	2020-08-10 13:07:01.005203+03	381	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-12, время начала: 10:30:00	1	[{"added": {}}]	7	350490234
279	2020-08-11 11:34:13.715546+03	391	Группа: НикитаШамаев, None, дата тренировки 2020-08-16, время начала: 15:30:00	3		7	350490234
280	2020-08-12 22:09:09.506924+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
1	2020-08-14 17:57:40.232809+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["status", "time_before_cancel"]}}]	6	350490234
2	2020-08-14 17:58:15.153164+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status", "time_before_cancel"]}}]	6	350490234
3	2020-08-16 21:18:16.026627+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["status"]}}]	6	638303006
4	2020-08-16 21:18:24.102067+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["status"]}}]	6	638303006
5	2020-08-16 21:28:01.866898+03	1	БАНДА №1, max_players: 6	1	[{"added": {}}]	9	638303006
6	2020-08-16 21:32:15.10806+03	1	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-08-18, время начала: 20:30:00	1	[{"added": {}}]	7	638303006
7	2020-08-16 21:39:49.387296+03	27	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-08-20, время начала: 20:30:00	1	[{"added": {}}]	7	638303006
8	2020-08-16 21:59:10.495351+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["status"]}}]	6	638303006
9	2020-08-16 21:59:54.393532+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["status"]}}]	6	638303006
10	2020-08-16 22:00:54.647947+03	1	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-08-18, время начала: 20:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	638303006
11	2020-08-16 22:10:09.77448+03	1	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-08-18, время начала: 20:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	638303006
12	2020-08-16 22:13:04.340311+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	638303006
13	2020-08-16 22:17:12.139642+03	2	ТестНикита, max_players: 1	1	[{"added": {}}]	9	638303006
14	2020-08-16 22:17:53.867626+03	3	Тест, max_players: 6	1	[{"added": {}}]	9	638303006
15	2020-08-16 22:18:14.917102+03	53	Группа: Тест, max_players: 6, дата тренировки 2020-08-16, время начала: 18:00:00	1	[{"added": {}}]	7	638303006
16	2020-08-16 22:19:09.419563+03	53	Группа: Тест, max_players: 6, дата тренировки 2020-08-16, время начала: 18:00:00	3		7	638303006
17	2020-08-16 22:19:25.187312+03	79	Группа: Тест, max_players: 6, дата тренировки 2020-08-17, время начала: 18:00:00	1	[{"added": {}}]	7	638303006
18	2020-08-16 22:20:17.960415+03	79	Группа: Тест, max_players: 6, дата тренировки 2020-08-17, время начала: 18:00:00	3		7	638303006
19	2020-08-17 22:55:23.962597+03	161750284	Юля Баранова -- 89207716766	2	[{"changed": {"fields": ["first_name", "last_name", "time_before_cancel"]}}]	6	638303006
20	2020-08-17 22:57:37.649185+03	638303006	Влад Юрков -- 89039600906	2	[{"changed": {"fields": ["first_name"]}}]	6	638303006
21	2020-08-17 22:57:44.355214+03	638303006	Влад Юрков -- 89039600906	2	[]	6	638303006
22	2020-08-17 23:00:21.586522+03	638303006	Влад Юрков -- 89039600906	2	[]	6	638303006
23	2020-08-17 23:00:55.472248+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["first_name"]}}]	6	638303006
24	2020-08-18 01:11:55.64512+03	105	Группа: БабаЯга, max_players: 1, дата тренировки 2020-08-19, время начала: 20:30:00	1	[{"added": {}}]	7	350490234
25	2020-08-18 11:07:35.57997+03	390	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-16, время начала: 15:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
26	2020-08-18 11:07:53.432062+03	390	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-16, время начала: 15:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
27	2020-08-18 11:08:12.112796+03	1803	НикитаШамаев, max_players: 1	2	[{"changed": {"fields": ["users"]}}]	9	350490234
28	2020-08-18 11:08:56.922993+03	393	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 18:00:00	2	[{"changed": {"fields": ["visitors", "is_available"]}}]	7	350490234
29	2020-08-18 11:09:04.472321+03	393	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
30	2020-08-18 11:09:39.724959+03	393	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
31	2020-08-18 11:09:44.892722+03	393	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
32	2020-08-18 11:12:04.36296+03	393	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
33	2020-08-18 11:12:09.615811+03	393	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
34	2020-08-18 11:37:45.64894+03	332	Группа: ОльгаШамаева, max_players: 1, дата тренировки 2020-08-01, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
35	2020-08-18 11:38:21.566979+03	332	Группа: ОльгаШамаева, max_players: 1, дата тренировки 2020-08-01, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
36	2020-08-18 11:38:30.892655+03	394	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 14:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
68	2020-08-18 11:58:30.721778+03	394	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 14:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
69	2020-08-18 12:00:02.884645+03	394	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-08-19, время начала: 14:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
70	2020-08-20 19:15:02.076373+03	1796	вторая, max_players: 4	2	[{"changed": {"fields": ["users"]}}]	9	350490234
71	2020-08-20 19:15:22.136564+03	123	aaaaaaaaaaaaaaa dddd -- 787978987987	2	[{"changed": {"fields": ["status"]}}, {"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (8)"}}]	6	350490234
72	2020-08-21 11:31:29.558029+03	123	aaaaaaaaaaaaaaa dddd -- 787978987987	2	[{"changed": {"fields": ["status"]}}]	6	350490234
73	2020-08-21 11:33:40.812794+03	123	aaaaaaaaaaaaaaa dddd -- 787978987987	2	[{"changed": {"fields": ["status"]}}]	6	350490234
74	2020-08-21 17:25:41.15314+03	364	Группа: вторая, max_players: 4, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
75	2020-08-21 17:28:54.993158+03	364	Группа: вторая, max_players: 4, дата тренировки 2020-08-23, время начала: 10:30:00	2	[]	7	350490234
76	2020-08-21 17:29:30.62053+03	364	Группа: вторая, max_players: 4, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
77	2020-08-21 17:29:59.574639+03	364	Группа: вторая, max_players: 4, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
78	2020-08-21 17:30:29.393577+03	364	Группа: вторая, max_players: 4, дата тренировки 2020-08-23, время начала: 10:30:00	2	[]	7	350490234
79	2020-08-21 17:30:36.385734+03	364	Группа: вторая, max_players: 4, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
80	2020-08-21 17:31:49.373643+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["max_players"]}}]	9	350490234
81	2020-08-21 17:42:17.962195+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
82	2020-08-21 17:42:58.51922+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
83	2020-08-21 17:48:37.682807+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
84	2020-08-21 17:48:48.167701+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
85	2020-08-21 17:54:26.757678+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
86	2020-08-21 17:54:31.291341+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
87	2020-08-21 17:55:59.145915+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
88	2020-08-21 17:56:38.615242+03	364	Группа: вторая, max_players: 6, дата тренировки 2020-08-23, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
89	2020-08-21 17:57:32.792412+03	231	Группа: Группа Никита Шамаев, max_players: 1, дата тренировки 2020-07-18, время начала: 16:30:00	3		7	350490234
90	2020-08-21 17:57:32.838895+03	232	Группа: Группа Никита Шамаев, max_players: 1, дата тренировки 2020-07-25, время начала: 16:30:00	3		7	350490234
91	2020-08-21 17:58:18.421153+03	1795	Группа Никита Шамаев, max_players: 1	3		9	350490234
92	2020-08-21 18:41:25.446704+03	354	Группа: третья, max_players: 4, дата тренировки 2020-08-27, время начала: 10:00:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
93	2020-08-21 20:32:06.891411+03	354	Группа: третья, max_players: 4, дата тренировки 2020-08-27, время начала: 10:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
94	2020-08-21 20:32:53.417621+03	354	Группа: третья, max_players: 4, дата тренировки 2020-08-27, время начала: 10:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
95	2020-08-21 20:33:36.061764+03	1801	БАНДА №3, max_players: 4	2	[{"changed": {"fields": ["name"]}}]	9	350490234
96	2020-08-21 20:35:20.446661+03	354	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-08-27, время начала: 10:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
97	2020-08-25 10:41:34.517855+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["add_info"]}}]	6	350490234
98	2020-08-25 12:22:06.638982+03	110	Группа: вторая, max_players: 6, дата тренировки 2020-08-25, время начала: 13:00:00	1	[{"added": {}}]	7	350490234
99	2020-08-25 12:55:37.318849+03	136	Группа: ОльгаШамаева, max_players: 1, дата тренировки 2020-08-26, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
100	2020-08-25 12:55:53.810811+03	136	Группа: ОльгаШамаева, max_players: 1, дата тренировки 2020-08-26, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
101	2020-08-25 12:57:29.229141+03	136	Группа: ОльгаШамаева, max_players: 1, дата тренировки 2020-08-26, время начала: 12:00:00	2	[{"changed": {"fields": ["is_individual"]}}]	7	350490234
102	2020-08-27 19:31:02.543937+03	107	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-09-03, время начала: 13:30:00	2	[{"changed": {"fields": ["is_individual"]}}]	7	350490234
103	2020-08-27 19:41:07.784175+03	328	Группа: Первая, max_players: 6, дата тренировки 2020-09-03, время начала: 16:30:00	3		7	350490234
104	2020-08-27 19:48:49.047876+03	138	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-09-03, время начала: 12:30:00	3		7	350490234
105	2020-08-27 19:49:30.555259+03	139	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-09-03, время начала: 11:30:00	3		7	350490234
106	2020-09-04 18:21:23.341011+03	1	Первая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
107	2020-09-04 18:22:33.214137+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (10)"}}]	6	350490234
108	2020-09-04 18:22:37.01956+03	350490234	Никита Шамаев -- 89661215215	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
109	2020-09-04 18:23:09.718105+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
110	2020-09-04 18:53:38.227137+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (11)"}}]	6	350490234
111	2020-09-04 18:53:52.072505+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
112	2020-09-04 18:54:00.086303+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
113	2020-09-04 18:54:18.950507+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (15)"}}]	6	350490234
114	2020-09-04 18:54:31.446456+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
115	2020-09-04 18:58:32.244216+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
116	2020-09-04 19:05:58.194376+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (17)"}}]	6	350490234
117	2020-09-04 19:07:56.76118+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (17)", "fields": ["traininggroup"]}}]	6	350490234
118	2020-09-04 19:17:11.325365+03	350490234	Никита Шамаев -- 89661215215	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
119	2020-09-04 19:22:45.61986+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (20)"}}]	6	350490234
475	2020-12-22 02:43:56.890258+03	382	фыв  -- 444444, месяц: 1	3		11	350490234
120	2020-09-04 19:25:00.60806+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
121	2020-09-04 19:25:16.803243+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (22)"}}]	6	350490234
122	2020-09-04 19:25:32.177514+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
123	2020-09-04 19:26:01.854518+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (23)"}}]	6	350490234
124	2020-09-04 19:26:12.141758+03	1	Первая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
125	2020-09-04 19:26:53.580203+03	3	фыв  -- 444444	2	[{"changed": {"fields": ["status"]}}, {"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (28)"}}]	6	350490234
126	2020-09-04 19:28:07.780576+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
127	2020-09-04 19:28:22.261968+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (29)"}}]	6	350490234
128	2020-09-04 19:28:34.913877+03	1796	вторая, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
129	2020-09-04 19:29:14.636941+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (30)"}}]	6	350490234
130	2020-09-04 19:29:33.725148+03	350490234	Никита Шамаев -- 89661215215	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
131	2020-09-04 19:30:18.780537+03	350490234	Никита Шамаев -- 89661215215	2	[]	6	350490234
132	2020-09-04 19:50:26.169757+03	1801	БАНДА №3, max_players: 4	2	[{"changed": {"fields": ["level"]}}]	9	350490234
133	2020-09-05 17:17:19.757385+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["parent"]}}]	6	350490234
134	2020-09-05 21:06:51.896912+03	143	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-09-03, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
135	2020-09-07 11:06:55.788779+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (31)"}}]	6	350490234
136	2020-09-07 11:27:31.716877+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
137	2020-09-07 11:29:26.443862+03	8	Кошка asd -- 789, месяц: 9	2	[]	11	350490234
138	2020-09-07 11:29:56.248153+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
139	2020-09-07 11:32:11.753507+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
140	2020-09-07 11:33:47.528435+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
141	2020-09-07 11:33:49.601547+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
142	2020-09-07 11:33:56.052454+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
143	2020-09-07 11:34:34.535103+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
144	2020-09-07 11:41:40.523441+03	385	Группа: вторая, max_players: 6, дата тренировки 2020-09-09, время начала: 10:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
145	2020-09-07 11:43:22.52335+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
146	2020-09-07 11:43:35.294116+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
147	2020-09-07 11:46:53.290984+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
148	2020-09-07 11:47:13.570281+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
149	2020-09-07 11:47:16.61041+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
150	2020-09-07 11:48:42.243777+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
151	2020-09-07 11:48:46.457231+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
152	2020-09-07 11:49:16.151841+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
153	2020-09-07 11:49:21.112062+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
154	2020-09-08 11:33:57.988043+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
155	2020-09-08 11:33:58.296274+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
156	2020-09-08 11:34:38.678184+03	1	Первая, max_players: 6	2	[{"changed": {"fields": ["status"]}}]	9	350490234
157	2020-09-08 11:35:06.572404+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
158	2020-09-08 11:36:11.010095+03	9	Никита Шамаев -- 89661215215, месяц: 9	2	[]	11	350490234
159	2020-09-08 11:52:11.207016+03	1	StaticData object (1)	1	[{"added": {}}]	12	350490234
160	2020-09-08 11:58:19.767979+03	2	StaticData object (2)	3		12	350490234
161	2020-09-08 12:00:25.432493+03	4	Ольга Шамаева -- 89611469010, месяц: 9	2	[]	11	350490234
162	2020-09-08 12:00:31.161629+03	36	Никита Шамаев -- 89661215215, месяц: 12	2	[]	11	350490234
163	2020-09-08 12:01:27.182327+03	13	Ольга Шамаева -- 89611469010, месяц: 10	2	[]	11	350490234
164	2020-09-19 13:04:14.467393+03	146	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-09-22, время начала: 16:00:00	3		7	350490234
165	2020-09-19 13:04:44.70864+03	166	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-09-20, время начала: 10:04:42	1	[{"added": {}}]	7	350490234
166	2020-09-19 13:06:50.175413+03	166	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-09-20, время начала: 10:04:42	3		7	350490234
167	2020-10-13 11:54:51.222495+03	118	Группа: вторая, max_players: 6, дата тренировки 2020-10-20, время начала: 13:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
168	2020-10-13 12:35:00.045883+03	118	Группа: вторая, max_players: 6, дата тренировки 2020-10-20, время начала: 13:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
169	2020-10-13 15:45:34.200507+03	118	Группа: вторая, max_players: 6, дата тренировки 2020-10-20, время начала: 13:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
170	2020-10-13 16:40:11.052581+03	348	Группа: Первая, max_players: 6, дата тренировки 2020-10-23, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
286	2020-10-22 13:02:49.340243+03	422	Группа: вторая, max_players: 6, дата тренировки 2020-10-22, время начала: 13:30:00	3		7	350490234
171	2020-10-13 16:40:31.465696+03	349	Группа: Первая, max_players: 6, дата тренировки 2020-10-30, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
172	2020-10-13 16:48:26.967609+03	119	Группа: вторая, max_players: 6, дата тренировки 2020-10-27, время начала: 13:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
173	2020-10-13 16:49:22.915787+03	224	Группа: вторая, max_players: 6, дата тренировки 2020-10-19, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
174	2020-10-13 16:49:31.827818+03	224	Группа: вторая, max_players: 6, дата тренировки 2020-10-19, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
175	2020-10-13 16:50:47.620756+03	250	Группа: вторая, max_players: 6, дата тренировки 2020-10-24, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
176	2020-10-13 16:51:25.779957+03	250	Группа: вторая, max_players: 6, дата тренировки 2020-10-24, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
177	2020-10-13 16:51:29.414671+03	250	Группа: вторая, max_players: 6, дата тренировки 2020-10-24, время начала: 12:00:00	2	[]	7	350490234
178	2020-10-13 17:01:51.51916+03	227	Группа: вторая, max_players: 6, дата тренировки 2020-11-09, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
179	2020-10-22 11:31:57.96061+03	395	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-23, время начала: 11:30:00	3		7	350490234
180	2020-10-22 11:31:58.105576+03	391	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-23, время начала: 13:30:00	3		7	350490234
287	2020-10-22 13:03:02.945314+03	448	Группа: вторая, max_players: 6, дата тренировки 2020-10-22, время начала: 14:10:00	1	[{"added": {}}]	7	350490234
291	2020-10-23 21:29:03.192815+03	494	Группа: Первая, max_players: 6, дата тренировки 2020-10-25, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
295	2020-10-23 22:15:00.145395+03	494	Группа: Первая, max_players: 6, дата тренировки 2020-10-25, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
299	2020-10-25 15:37:57.655518+03	1	Первая, max_players: 6	2	[{"changed": {"fields": ["status"]}}]	9	350490234
303	2020-10-25 16:11:18.392299+03	18	Никита Шамаев -- 89661215215, месяц: 10	2	[{"changed": {"fields": ["fact_amount"]}}]	11	350490234
307	2020-10-26 18:08:47.851174+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-11-01, время начала: 13:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
311	2020-10-26 18:18:31.74436+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-11-02, время начала: 14:30:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
315	2020-10-26 18:26:11.109679+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-28, время начала: 14:30:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
319	2020-10-26 18:30:59.675857+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-28, время начала: 14:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
323	2020-10-26 18:35:25.927291+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-28, время начала: 15:30:00	2	[{"changed": {"fields": ["date", "start_time", "duration"]}}]	7	350490234
327	2020-10-26 21:50:33.220558+03	359	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-10-01, время начала: 10:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
331	2020-10-31 01:59:13.636782+03	350490234	Никита Шамаев -- 89661215215	2	[]	6	350490234
335	2020-11-09 20:29:42.716854+03	563	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-11-16, время начала: 18:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
337	2020-11-22 18:10:50.999284+03	564	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-11-23, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
340	2020-11-22 18:18:51.24635+03	350490234	Никита Шамаев -- 89661215215	2	[]	6	350490234
343	2020-11-22 18:23:56.149479+03	229	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-11-23, время начала: 12:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
346	2020-11-29 20:28:54.487353+03	565	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-11-30, время начала: 21:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
349	2020-11-29 20:30:12.689866+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
352	2020-11-29 20:32:21.744346+03	499	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-11-29, время начала: 23:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
355	2020-11-30 14:19:34.579132+03	230	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-11-30, время начала: 15:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
358	2020-12-01 01:09:16.121755+03	1	БАНДА №1, max_players: 6	2	[{"changed": {"fields": ["tarif_for_one_lesson"]}}]	9	350490234
360	2020-12-07 18:55:30.366479+03	454	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-03, время начала: 14:10:00	2	[]	7	350490234
363	2020-12-07 19:44:57.73872+03	596	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-12, время начала: 18:30:00	2	[]	7	350490234
366	2020-12-07 19:51:02.82709+03	612	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 16:50:39	1	[{"added": {}}]	7	350490234
369	2020-12-07 19:59:44.910488+03	638	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-07, время начала: 18:00:00	3		7	350490234
372	2020-12-07 20:01:30.09239+03	690	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
375	2020-12-07 20:03:23.877895+03	716	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 18:00:00	3		7	350490234
378	2020-12-07 20:04:28.328185+03	768	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
381	2020-12-07 20:06:42.080916+03	794	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
384	2020-12-07 20:09:41.765108+03	820	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
288	2020-10-22 13:03:39.060514+03	448	Группа: вторая, max_players: 6, дата тренировки 2020-10-22, время начала: 14:10:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
292	2020-10-23 22:12:59.933921+03	181	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-25, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
296	2020-10-23 22:17:01.516712+03	494	Группа: Первая, max_players: 6, дата тренировки 2020-10-25, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
300	2020-10-25 15:38:13.74232+03	1	БАНДА №1, max_players: 6	2	[{"changed": {"fields": ["name"]}}]	9	350490234
304	2020-10-25 17:42:03.561768+03	1329	Пробная Оплата -- 1235123512	1	[{"added": {}}]	6	350490234
308	2020-10-26 18:13:03.725314+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-11-01, время начала: 14:00:00	2	[{"changed": {"fields": ["start_time", "duration"]}}]	7	350490234
312	2020-10-26 18:18:49.436287+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-29, время начала: 14:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
316	2020-10-26 18:29:17.689306+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-29, время начала: 14:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
320	2020-10-26 18:31:42.708285+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-29, время начала: 14:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
324	2020-10-26 21:40:51.485102+03	1	БАНДА №1, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
328	2020-10-26 22:10:33.399636+03	586	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-03, время начала: 18:30:00	1	[{"added": {}}]	7	350490234
332	2020-11-03 23:06:08.6796+03	1329	Пробная Оплата -- 1235123512	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (34)"}}]	6	350490234
338	2020-11-22 18:11:34.776797+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
341	2020-11-22 18:19:12.791095+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
344	2020-11-29 20:07:04.599658+03	1	БАНДА №1, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
347	2020-11-29 20:29:12.256173+03	565	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-11-30, время начала: 21:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
350	2020-11-29 20:31:03.292742+03	565	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-11-30, время начала: 21:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
353	2020-11-30 13:58:42.488854+03	230	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-11-30, время начала: 12:00:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
356	2020-11-30 17:16:37.832569+03	230	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-11-30, время начала: 18:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
361	2020-12-07 19:21:21.972702+03	566	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-07, время начала: 19:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
364	2020-12-07 19:48:27.113733+03	454	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-03, время начала: 14:10:00	2	[]	7	350490234
367	2020-12-07 19:51:30.298309+03	612	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 16:50:39	3		7	350490234
370	2020-12-07 20:00:43.244753+03	664	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-07, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
373	2020-12-07 20:02:08.727544+03	690	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 18:00:00	3		7	350490234
376	2020-12-07 20:03:39.15326+03	742	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
379	2020-12-07 20:04:45.873571+03	768	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
382	2020-12-07 20:07:53.148539+03	500	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-06, время начала: 12:00:00	2	[]	7	350490234
385	2020-12-07 20:10:53.499951+03	846	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
387	2020-12-07 20:15:26.129019+03	500	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-06, время начала: 12:00:00	2	[]	7	350490234
389	2020-12-07 21:08:45.983085+03	872	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
391	2020-12-07 21:10:01.771771+03	898	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
393	2020-12-07 21:11:46.062649+03	899	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
395	2020-12-08 00:17:35.496315+03	231	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-07, время начала: 12:00:00	3		7	350490234
397	2020-12-08 00:18:54.733103+03	925	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
399	2020-12-08 00:19:33.598467+03	926	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
400	2020-12-22 02:01:40.241961+03	350490234	Никита Шамаев -- 89661215215	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
402	2020-12-22 02:04:03.725648+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
403	2020-12-22 02:04:31.14663+03	350490234	Никита Шамаев -- 89661215215	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (35)"}}]	6	350490234
404	2020-12-22 02:05:31.743718+03	350490234	Никита Шамаев -- 89661215215	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
405	2020-12-22 02:05:47.175865+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
406	2020-12-22 02:36:23.557066+03	6	БАНДА №4, max_players: 2	1	[{"added": {}}]	9	350490234
289	2020-10-22 13:03:59.756924+03	448	Группа: вторая, max_players: 6, дата тренировки 2020-10-22, время начала: 13:30:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
293	2020-10-23 22:13:03.920942+03	494	Группа: Первая, max_players: 6, дата тренировки 2020-10-25, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
297	2020-10-23 22:31:56.875601+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
301	2020-10-25 15:38:31.950458+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["name"]}}]	9	350490234
305	2020-10-25 17:43:49.292438+03	350490234	Никита Шамаев -- 89661215215	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
309	2020-10-26 18:15:42.524923+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-11-02, время начала: 14:00:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
313	2020-10-26 18:19:12.411196+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-29, время начала: 18:30:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
317	2020-10-26 18:29:43.826416+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-28, время начала: 14:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
321	2020-10-26 18:33:01.8686+03	495	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-10-28, время начала: 14:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
325	2020-10-26 21:41:09.03384+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
329	2020-10-31 01:57:29.337302+03	1	БАНДА №1, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
333	2020-11-03 23:09:56.34029+03	37	Пробная Оплата -- 1235123512, месяц: 11	3		11	350490234
336	2020-11-22 18:10:39.51293+03	229	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-11-23, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
339	2020-11-22 18:12:55.348555+03	488	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-11-25, время начала: 18:30:00	2	[{"changed": {"fields": ["is_individual"]}}]	7	350490234
342	2020-11-22 18:20:44.080059+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
345	2020-11-29 20:15:51.688364+03	124	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-01, время начала: 13:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
348	2020-11-29 20:29:52.679651+03	565	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-11-30, время начала: 21:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
351	2020-11-29 20:32:06.44473+03	499	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-11-29, время начала: 21:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
354	2020-11-30 14:00:24.401704+03	230	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-11-30, время начала: 15:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
357	2020-12-01 01:05:47.201307+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
359	2020-12-07 18:54:42.954341+03	454	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-03, время начала: 14:10:00	2	[]	7	350490234
362	2020-12-07 19:40:01.863017+03	350490234	Никита Шамаев -- 89661215215	2	[]	6	350490234
365	2020-12-07 19:50:12.626258+03	231	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-07, время начала: 12:00:00	2	[]	7	350490234
368	2020-12-07 19:59:05.390572+03	638	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-07, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
371	2020-12-07 20:01:16.980059+03	664	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-07, время начала: 18:00:00	3		7	350490234
374	2020-12-07 20:03:10.972914+03	716	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
377	2020-12-07 20:04:02.007583+03	742	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-09, время начала: 18:00:00	3		7	350490234
380	2020-12-07 20:06:27.704962+03	794	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
383	2020-12-07 20:08:58.492034+03	820	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
386	2020-12-07 20:11:29.167048+03	846	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
388	2020-12-07 20:16:16.945579+03	500	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-06, время начала: 12:00:00	2	[]	7	350490234
281	2020-10-22 11:32:58.49617+03	395	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-23, время начала: 11:30:00	3		7	350490234
282	2020-10-22 11:32:58.508622+03	391	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-23, время начала: 13:30:00	3		7	350490234
283	2020-10-22 11:32:58.520193+03	328	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-23, время начала: 14:30:00	3		7	350490234
284	2020-10-22 11:32:58.530953+03	315	Группа: НикитаШамаев, max_players: 1, дата тренировки 2020-10-23, время начала: 14:30:00	3		7	350490234
390	2020-12-07 21:09:14.178132+03	872	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
392	2020-12-07 21:11:30.467594+03	898	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
394	2020-12-07 21:11:57.439091+03	899	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	3		7	350490234
396	2020-12-08 00:17:51.304076+03	567	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-14, время начала: 18:00:00	3		7	350490234
398	2020-12-08 00:19:19.053524+03	926	Группа: БАНДА №1, max_players: 6, дата тренировки 2020-12-04, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
401	2020-12-22 02:03:26.820923+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}, {"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
407	2020-12-22 02:37:12.599065+03	1329	Пробная Оплата -- 1235123512	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
408	2020-12-22 02:37:28.665643+03	1329	Пробная Оплата -- 1235123512	2	[{"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
409	2020-12-22 02:37:48.643673+03	1329	Пробная Оплата -- 1235123512	2	[{"changed": {"fields": ["status"]}}]	6	350490234
410	2020-12-22 02:41:05.602612+03	341	klfflkfkk  -- 1213213214, месяц: 11	3		11	350490234
411	2020-12-22 02:41:05.694026+03	340	Крекс asd -- 789456, месяц: 11	3		11	350490234
412	2020-12-22 02:41:05.705144+03	339	фыв  -- 444444, месяц: 11	3		11	350490234
413	2020-12-22 02:41:05.716346+03	338	Баба Яга -- 214141, месяц: 11	3		11	350490234
414	2020-12-22 02:41:05.727597+03	337	Владлен Юрков -- 89039600906, месяц: 11	3		11	350490234
415	2020-12-22 02:41:05.738507+03	336	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 11	3		11	350490234
416	2020-12-22 02:41:05.749507+03	335	Никита Шамаев -- 89661215215, месяц: 11	3		11	350490234
417	2020-12-22 02:41:05.760696+03	334	Пробная Оплата -- 1235123512, месяц: 11	3		11	350490234
418	2020-12-22 02:41:05.771844+03	333	Ольга Шамаева -- 89611469010, месяц: 11	3		11	350490234
419	2020-12-22 02:41:05.783109+03	332	Кошка asd -- 789, месяц: 11	3		11	350490234
420	2020-12-22 02:41:05.794069+03	280	klfflkfkk  -- 1213213214, месяц: 4	3		11	350490234
421	2020-12-22 02:41:05.805231+03	279	Крекс asd -- 789456, месяц: 4	3		11	350490234
422	2020-12-22 02:41:05.81665+03	278	фыв  -- 444444, месяц: 4	3		11	350490234
423	2020-12-22 02:41:05.827245+03	277	Баба Яга -- 214141, месяц: 4	3		11	350490234
424	2020-12-22 02:41:05.838515+03	276	Владлен Юрков -- 89039600906, месяц: 4	3		11	350490234
425	2020-12-22 02:41:05.849833+03	275	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 4	3		11	350490234
426	2020-12-22 02:41:05.860649+03	274	Пробная Оплата -- 1235123512, месяц: 4	3		11	350490234
427	2020-12-22 02:41:05.872056+03	273	Ольга Шамаева -- 89611469010, месяц: 4	3		11	350490234
428	2020-12-22 02:41:05.882957+03	272	Кошка asd -- 789, месяц: 4	3		11	350490234
429	2020-12-22 02:41:05.894033+03	271	klfflkfkk  -- 1213213214, месяц: 4	3		11	350490234
430	2020-12-22 02:41:05.905366+03	270	Крекс asd -- 789456, месяц: 4	3		11	350490234
431	2020-12-22 02:41:05.916336+03	269	фыв  -- 444444, месяц: 4	3		11	350490234
432	2020-12-22 02:41:05.927357+03	268	Баба Яга -- 214141, месяц: 4	3		11	350490234
433	2020-12-22 02:41:05.938725+03	267	Владлен Юрков -- 89039600906, месяц: 4	3		11	350490234
434	2020-12-22 02:41:05.949651+03	266	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 4	3		11	350490234
435	2020-12-22 02:41:05.960723+03	265	Пробная Оплата -- 1235123512, месяц: 4	3		11	350490234
436	2020-12-22 02:41:05.972248+03	264	Ольга Шамаева -- 89611469010, месяц: 4	3		11	350490234
437	2020-12-22 02:41:05.982981+03	263	Кошка asd -- 789, месяц: 4	3		11	350490234
438	2020-12-22 02:41:05.993992+03	262	klfflkfkk  -- 1213213214, месяц: 4	3		11	350490234
439	2020-12-22 02:41:06.005584+03	261	Крекс asd -- 789456, месяц: 4	3		11	350490234
440	2020-12-22 02:41:06.09458+03	260	фыв  -- 444444, месяц: 4	3		11	350490234
441	2020-12-22 02:41:06.105386+03	259	Баба Яга -- 214141, месяц: 4	3		11	350490234
442	2020-12-22 02:41:06.116452+03	258	Владлен Юрков -- 89039600906, месяц: 4	3		11	350490234
443	2020-12-22 02:41:06.127598+03	257	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 4	3		11	350490234
444	2020-12-22 02:41:06.138726+03	256	Пробная Оплата -- 1235123512, месяц: 4	3		11	350490234
445	2020-12-22 02:41:06.149907+03	255	Никита Шамаев -- 89661215215, месяц: 4	3		11	350490234
446	2020-12-22 02:41:06.161212+03	254	Ольга Шамаева -- 89611469010, месяц: 4	3		11	350490234
447	2020-12-22 02:41:06.172045+03	253	Кошка asd -- 789, месяц: 4	3		11	350490234
448	2020-12-22 02:41:06.183216+03	252	Кошка asd -- 789, месяц: 4	3		11	350490234
449	2020-12-22 02:41:06.194256+03	251	фыв  -- 444444, месяц: 4	3		11	350490234
450	2020-12-22 02:41:06.20544+03	250	Баба Яга -- 214141, месяц: 4	3		11	350490234
451	2020-12-22 02:41:06.216524+03	249	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 4	3		11	350490234
452	2020-12-22 02:41:06.227623+03	248	Никита Шамаев -- 89661215215, месяц: 9	3		11	350490234
453	2020-12-22 02:41:06.238901+03	247	Ольга Шамаева -- 89611469010, месяц: 9	3		11	350490234
454	2020-12-22 02:41:06.249861+03	246	Крекс asd -- 789456, месяц: 9	3		11	350490234
455	2020-12-22 02:41:06.260958+03	245	Пробная Оплата -- 1235123512, месяц: 9	3		11	350490234
456	2020-12-22 02:41:06.272183+03	244	klfflkfkk  -- 1213213214, месяц: 9	3		11	350490234
457	2020-12-22 02:41:06.283368+03	243	Владлен Юрков -- 89039600906, месяц: 9	3		11	350490234
458	2020-12-22 02:41:06.294415+03	242	Кошка asd -- 789, месяц: 9	3		11	350490234
459	2020-12-22 02:41:06.305751+03	241	фыв  -- 444444, месяц: 9	3		11	350490234
460	2020-12-22 02:41:06.316946+03	240	Баба Яга -- 214141, месяц: 9	3		11	350490234
461	2020-12-22 02:41:06.327814+03	239	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 9	3		11	350490234
462	2020-12-22 02:41:06.339211+03	238	Никита Шамаев -- 89661215215, месяц: 1	3		11	350490234
463	2020-12-22 02:41:06.349911+03	237	Ольга Шамаева -- 89611469010, месяц: 1	3		11	350490234
464	2020-12-22 02:41:06.361107+03	236	Крекс asd -- 789456, месяц: 1	3		11	350490234
465	2020-12-22 02:41:06.372222+03	235	Пробная Оплата -- 1235123512, месяц: 1	3		11	350490234
466	2020-12-22 02:41:06.383235+03	234	klfflkfkk  -- 1213213214, месяц: 1	3		11	350490234
467	2020-12-22 02:41:06.394572+03	233	Владлен Юрков -- 89039600906, месяц: 1	3		11	350490234
468	2020-12-22 02:41:06.405666+03	232	Кошка asd -- 789, месяц: 1	3		11	350490234
469	2020-12-22 02:41:06.416606+03	231	фыв  -- 444444, месяц: 1	3		11	350490234
470	2020-12-22 02:41:06.427822+03	230	Баба Яга -- 214141, месяц: 1	3		11	350490234
471	2020-12-22 02:41:06.438887+03	229	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 1	3		11	350490234
472	2020-12-22 02:42:06.431191+03	1329	Пробная Оплата -- 1235123512	2	[{"added": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (38)"}}]	6	350490234
473	2020-12-22 02:43:56.804145+03	384	klfflkfkk  -- 1213213214, месяц: 1	3		11	350490234
474	2020-12-22 02:43:56.879229+03	383	Крекс asd -- 789456, месяц: 1	3		11	350490234
476	2020-12-22 02:43:56.979259+03	381	Баба Яга -- 214141, месяц: 1	3		11	350490234
477	2020-12-22 02:43:56.990242+03	380	Владлен Юрков -- 89039600906, месяц: 1	3		11	350490234
478	2020-12-22 02:43:57.001591+03	379	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 1	3		11	350490234
479	2020-12-22 02:43:57.012422+03	378	Пробная Оплата -- 1235123512, месяц: 1	3		11	350490234
480	2020-12-22 02:43:57.023435+03	377	Ольга Шамаева -- 89611469010, месяц: 1	3		11	350490234
481	2020-12-22 02:43:57.034771+03	376	Кошка asd -- 789, месяц: 1	3		11	350490234
482	2020-12-22 02:43:57.046042+03	375	klfflkfkk  -- 1213213214, месяц: 1	3		11	350490234
483	2020-12-22 02:43:57.0571+03	374	Крекс asd -- 789456, месяц: 1	3		11	350490234
484	2020-12-22 02:43:57.068299+03	373	фыв  -- 444444, месяц: 1	3		11	350490234
485	2020-12-22 02:43:57.079065+03	372	Баба Яга -- 214141, месяц: 1	3		11	350490234
486	2020-12-22 02:43:57.090211+03	371	Владлен Юрков -- 89039600906, месяц: 1	3		11	350490234
487	2020-12-22 02:43:57.101451+03	370	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 1	3		11	350490234
488	2020-12-22 02:43:57.112523+03	369	Пробная Оплата -- 1235123512, месяц: 1	3		11	350490234
489	2020-12-22 02:43:57.123619+03	368	Ольга Шамаева -- 89611469010, месяц: 1	3		11	350490234
490	2020-12-22 02:43:57.135509+03	367	Кошка asd -- 789, месяц: 1	3		11	350490234
491	2020-12-22 02:43:57.145809+03	366	klfflkfkk  -- 1213213214, месяц: 1	3		11	350490234
492	2020-12-22 02:43:57.157511+03	365	Крекс asd -- 789456, месяц: 1	3		11	350490234
493	2020-12-22 02:43:57.168497+03	364	фыв  -- 444444, месяц: 1	3		11	350490234
494	2020-12-22 02:43:57.179212+03	363	Баба Яга -- 214141, месяц: 1	3		11	350490234
495	2020-12-22 02:43:57.190316+03	362	Владлен Юрков -- 89039600906, месяц: 1	3		11	350490234
496	2020-12-22 02:43:57.201865+03	361	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 1	3		11	350490234
497	2020-12-22 02:43:57.212483+03	360	Пробная Оплата -- 1235123512, месяц: 1	3		11	350490234
498	2020-12-22 02:43:57.223792+03	359	Ольга Шамаева -- 89611469010, месяц: 1	3		11	350490234
499	2020-12-22 02:43:57.235368+03	358	Кошка asd -- 789, месяц: 1	3		11	350490234
500	2020-12-22 02:43:57.245946+03	357	klfflkfkk  -- 1213213214, месяц: 1	3		11	350490234
501	2020-12-22 02:43:57.25701+03	356	Крекс asd -- 789456, месяц: 1	3		11	350490234
502	2020-12-22 02:43:57.268832+03	355	фыв  -- 444444, месяц: 1	3		11	350490234
503	2020-12-22 02:43:57.279253+03	354	Баба Яга -- 214141, месяц: 1	3		11	350490234
504	2020-12-22 02:43:57.2904+03	353	Владлен Юрков -- 89039600906, месяц: 1	3		11	350490234
505	2020-12-22 02:43:57.302098+03	352	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 1	3		11	350490234
506	2020-12-22 02:43:57.312595+03	351	Никита Шамаев -- 89661215215, месяц: 1	3		11	350490234
507	2020-12-22 02:43:57.323741+03	350	Пробная Оплата -- 1235123512, месяц: 1	3		11	350490234
508	2020-12-22 02:43:57.33518+03	349	Ольга Шамаева -- 89611469010, месяц: 1	3		11	350490234
509	2020-12-22 02:43:57.346096+03	348	Кошка asd -- 789, месяц: 1	3		11	350490234
510	2020-12-22 02:43:57.357171+03	347	klfflkfkk  -- 1213213214, месяц: 1	3		11	350490234
511	2020-12-22 02:43:57.368476+03	346	Владлен Юрков -- 89039600906, месяц: 1	3		11	350490234
512	2020-12-22 02:43:57.379504+03	345	Кошка asd -- 789, месяц: 1	3		11	350490234
513	2020-12-22 02:43:57.390556+03	344	фыв  -- 444444, месяц: 1	3		11	350490234
514	2020-12-22 02:43:57.401898+03	343	Баба Яга -- 214141, месяц: 1	3		11	350490234
515	2020-12-22 02:43:57.412848+03	342	aaaaaaaaaaaaaaa dddd -- 787978987987, месяц: 1	3		11	350490234
516	2020-12-22 19:40:16.112691+03	8	Детская банда, max_players: 2	1	[{"added": {}}]	9	350490234
517	2020-12-22 19:40:31.269461+03	8	Детская банда, max_players: 3	2	[{"changed": {"fields": ["max_players"]}}]	9	350490234
518	2020-12-25 16:37:38.852719+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (39)", "fields": ["traininggroup"]}}]	6	350490234
519	2020-12-25 16:38:42.592142+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
520	2020-12-25 16:38:51.693573+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
521	2020-12-25 17:03:58.039047+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
522	2020-12-25 17:04:11.546225+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
523	2020-12-25 17:04:22.632787+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
524	2020-12-25 17:04:29.514508+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
525	2020-12-25 17:05:10.820445+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
526	2020-12-25 17:05:16.079772+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
527	2020-12-25 17:06:27.507603+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
528	2020-12-25 17:06:33.677034+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
529	2020-12-25 17:06:48.392139+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
530	2020-12-25 17:06:52.233492+03	965	Группа: БАНДА №3, max_players: 4, дата тренировки 2020-12-28, время начала: 18:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
531	2020-12-25 17:09:22.290246+03	128	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-29, время начала: 13:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
532	2020-12-25 17:18:54.341968+03	128	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-29, время начала: 13:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
533	2020-12-25 17:47:46.36081+03	1796	БАНДА №2, max_players: 6	2	[]	9	350490234
534	2020-12-25 17:58:45.031101+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
535	2020-12-25 17:59:54.087525+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
536	2020-12-25 18:00:29.383882+03	128	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-29, время начала: 13:00:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
537	2020-12-25 18:00:43.929214+03	1796	БАНДА №2, max_players: 6	2	[]	9	350490234
538	2020-12-25 18:11:57.066542+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
539	2020-12-25 18:12:05.946246+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
540	2020-12-25 18:13:35.448178+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
541	2020-12-25 18:13:42.166915+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
542	2020-12-25 18:25:53.825276+03	1796	БАНДА №2, max_players: 6	2	[]	9	350490234
543	2020-12-25 18:37:07.592246+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
544	2020-12-25 18:37:18.583668+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
545	2020-12-25 18:47:25.383247+03	1796	БАНДА №2, max_players: 6	2	[]	9	350490234
546	2020-12-25 19:04:14.211817+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
547	2020-12-25 19:04:35.891973+03	1796	БАНДА №2, max_players: 6	2	[]	9	350490234
548	2020-12-25 19:04:39.715341+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
549	2020-12-25 19:04:43.622884+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
550	2020-12-25 19:04:47.711459+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
551	2020-12-25 19:04:50.983687+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
552	2020-12-25 19:05:38.254006+03	128	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-29, время начала: 13:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
553	2020-12-25 19:06:44.320184+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
554	2020-12-25 19:06:54.000513+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
555	2020-12-25 19:07:38.541658+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["users"]}}]	9	350490234
556	2020-12-25 19:07:43.150011+03	128	Группа: БАНДА №2, max_players: 6, дата тренировки 2020-12-29, время начала: 13:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
557	2021-01-13 01:23:52.562447+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
558	2021-01-19 20:41:02.246208+03	1796	БАНДА №2, max_players: 6	2	[{"changed": {"fields": ["available_for_additional_lessons"]}}]	9	350490234
559	2021-01-19 21:15:37.679367+03	1796	БАНДА №2, max_players: 5	2	[{"changed": {"fields": ["max_players"]}}]	9	350490234
560	2021-01-19 21:31:25.804686+03	1796	БАНДА №2, max_players: 4	2	[{"changed": {"fields": ["users", "max_players"]}}]	9	350490234
561	2021-01-19 21:37:55.625186+03	132	Группа: БАНДА №2, max_players: 4, дата тренировки 2021-01-26, время начала: 13:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
562	2021-01-19 21:39:29.314537+03	132	Группа: БАНДА №2, max_players: 4, дата тренировки 2021-01-26, время начала: 13:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
563	2021-01-19 21:42:59.315594+03	132	Группа: БАНДА №2, max_players: 4, дата тренировки 2021-01-26, время начала: 13:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
564	2021-01-19 21:44:19.594236+03	6	БАНДА №4, max_players: 5	2	[{"changed": {"fields": ["users", "max_players", "available_for_additional_lessons"]}}]	9	350490234
565	2021-01-19 21:44:52.516941+03	1	БАНДА №1, max_players: 5	2	[{"changed": {"fields": ["users", "max_players"]}}]	9	350490234
566	2021-01-19 21:46:40.380566+03	603	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-30, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
567	2021-01-19 21:47:45.861826+03	1	БАНДА №1, max_players: 5	2	[{"changed": {"fields": ["available_for_additional_lessons"]}}]	9	350490234
568	2021-01-20 23:51:31.320935+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
569	2021-01-20 23:51:55.144005+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
570	2021-01-20 23:52:17.673254+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
571	2021-01-20 23:52:23.634483+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
572	2021-01-20 23:54:25.474242+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
573	2021-01-21 00:04:31.865764+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
574	2021-01-21 00:05:25.59823+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
575	2021-01-21 00:05:59.316691+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
576	2021-01-21 00:06:59.007101+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
577	2021-01-21 00:08:55.136225+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
578	2021-01-21 00:11:27.919132+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
579	2021-01-21 00:14:42.757553+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
580	2021-01-21 00:16:45.8112+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
581	2021-01-21 00:18:06.546694+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["pay_visitors"]}}]	7	350490234
582	2021-01-21 00:32:49.460848+03	602	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-01-23, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
583	2021-02-03 22:47:18.823071+03	1	БАНДА №1, max_players: 5	2	[{"changed": {"fields": ["users"]}}]	9	350490234
584	2021-02-03 22:47:46.63329+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["pay_visitors"]}}]	7	350490234
585	2021-02-04 01:11:09.721309+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
586	2021-02-04 01:13:01.694825+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent", "visitors", "pay_visitors"]}}]	7	350490234
587	2021-02-04 01:13:10.140522+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[]	7	350490234
588	2021-02-04 01:14:03.601157+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent", "pay_visitors"]}}]	7	350490234
589	2021-02-04 01:15:18.866712+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
590	2021-02-04 01:16:31.469472+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors", "pay_visitors"]}}]	7	350490234
591	2021-02-04 01:17:03.355212+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
592	2021-02-04 01:17:44.682054+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
593	2021-02-04 01:18:21.320103+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors", "pay_visitors"]}}]	7	350490234
594	2021-02-04 01:18:25.921334+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors", "pay_visitors"]}}]	7	350490234
595	2021-02-04 01:19:24.455093+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["pay_visitors"]}}]	7	350490234
596	2021-02-04 01:21:09.967728+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
597	2021-02-04 01:21:35.426639+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}, {"deleted": {"name": "\\u0421\\u0432\\u044f\\u0437\\u044c traininggroup-user", "object": "TrainingGroup_users object (None)"}}]	6	350490234
598	2021-02-04 01:22:23.675558+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
599	2021-02-04 01:46:07.087053+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
600	2021-02-04 01:46:26.365662+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors", "pay_visitors"]}}]	7	350490234
601	2021-02-04 01:46:48.736398+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
602	2021-02-04 01:47:01.749004+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
603	2021-02-04 01:48:59.73652+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["visitors", "pay_visitors"]}}]	7	350490234
604	2021-02-04 01:49:29.382777+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
605	2021-02-04 01:49:49.546273+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["pay_visitors"]}}]	7	350490234
606	2021-02-04 01:50:48.377588+03	1	БАНДА №1, max_players: 5	2	[{"changed": {"fields": ["users"]}}]	9	350490234
607	2021-02-04 01:53:56.336369+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent", "pay_visitors"]}}]	7	350490234
608	2021-02-04 01:54:21.144619+03	604	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-06, время начала: 18:30:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
609	2021-02-04 02:01:53.070165+03	6	БАНДА №4, max_players: 3	2	[{"changed": {"fields": ["users", "max_players"]}}]	9	350490234
610	2021-02-04 02:03:05.640021+03	966	Группа: БАНДА №4, max_players: 3, дата тренировки 2021-02-05, время начала: 13:00:00	1	[{"added": {}}]	7	350490234
611	2021-02-04 02:19:57.324296+03	509	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-07, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
612	2021-02-04 02:20:13.11884+03	509	Группа: БАНДА №1, max_players: 5, дата тренировки 2021-02-07, время начала: 12:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
613	2021-02-06 11:45:54.144761+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
614	2021-02-06 11:47:22.780422+03	6	БАНДА №4, max_players: 4	2	[{"changed": {"fields": ["users", "max_players"]}}]	9	350490234
615	2021-02-06 11:49:50.127178+03	456	Никита Шамаев -- 89661215215, месяц: 2	2	[{"changed": {"fields": ["fact_amount"]}}]	11	350490234
616	2021-02-06 11:56:52.881666+03	456	Никита Шамаев -- 89661215215, месяц: 2	2	[{"changed": {"fields": ["fact_amount"]}}]	11	350490234
617	2021-02-06 11:58:43.255968+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
618	2021-02-06 12:02:55.167607+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
619	2021-02-06 12:03:34.903895+03	456	Никита Шамаев -- 89661215215, месяц: 2	2	[{"changed": {"fields": ["fact_amount"]}}]	11	350490234
620	2021-02-06 12:17:36.535845+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
621	2021-02-06 12:17:58.282813+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	base	user
7	base	grouptrainingday
8	base	tarif
9	base	traininggroup
10	base	channel
11	base	payment
12	base	staticdata
13	base	alertslog
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-07-14 15:29:50.89144+03
2	contenttypes	0002_remove_content_type_name	2020-07-14 15:29:50.923529+03
3	auth	0001_initial	2020-07-14 15:29:51.581241+03
4	auth	0002_alter_permission_name_max_length	2020-07-14 15:29:51.601928+03
5	auth	0003_alter_user_email_max_length	2020-07-14 15:29:51.619533+03
6	auth	0004_alter_user_username_opts	2020-07-14 15:29:51.631859+03
7	auth	0005_alter_user_last_login_null	2020-07-14 15:29:51.654455+03
8	auth	0006_require_contenttypes_0002	2020-07-14 15:29:51.668912+03
9	auth	0007_alter_validators_add_error_messages	2020-07-14 15:29:51.691188+03
10	auth	0008_alter_user_username_max_length	2020-07-14 15:29:51.707432+03
11	auth	0009_alter_user_last_name_max_length	2020-07-14 15:29:51.719296+03
12	base	0001_initial	2020-07-14 15:29:53.693485+03
13	admin	0001_initial	2020-07-14 15:29:54.039102+03
14	admin	0002_logentry_remove_auto_add	2020-07-14 15:29:54.067145+03
15	sessions	0001_initial	2020-07-14 15:29:54.362592+03
16	base	0002_auto_20200714_1331	2020-07-14 16:32:05.208665+03
17	base	0003_auto_20200714_2043	2020-07-14 23:43:33.178087+03
18	base	0004_auto_20200714_2051	2020-07-14 23:51:21.862221+03
19	base	0005_channel	2020-07-15 11:17:40.993903+03
20	base	0006_auto_20200715_2151	2020-07-16 01:03:50.470152+03
21	base	0007_auto_20200716_1025	2020-07-16 13:25:08.191448+03
22	base	0008_auto_20200801_1113	2020-08-01 14:15:24.59089+03
23	base	0009_auto_20200812_1834	2020-08-12 21:34:32.800892+03
25	base	0010_auto_20200818_0712	2020-08-18 10:13:08.699255+03
26	base	0011_auto_20200818_0924	2020-08-18 12:24:44.902347+03
27	base	0012_auto_20200818_0932	2020-08-18 12:32:11.916366+03
28	base	0013_auto_20200818_1008	2020-08-18 13:08:37.752113+03
29	base	0014_payment	2020-08-25 11:49:54.66745+03
30	base	0015_auto_20200825_0849	2020-08-25 11:49:54.699206+03
31	base	0016_auto_20200825_0903	2020-08-25 12:03:28.293694+03
32	base	0017_grouptrainingday_is_individual	2020-08-25 12:54:40.439805+03
33	base	0018_auto_20200904_1422	2020-09-04 17:27:25.932072+03
34	base	0019_set_group_status	2020-09-04 17:30:49.896242+03
35	base	0020_auto_20200904_1432	2020-09-04 17:32:45.791389+03
36	base	0021_traininggroup_level	2020-09-04 19:40:03.249261+03
37	base	0022_auto_20200904_1650	2020-09-04 19:50:05.76659+03
38	base	0023_auto_20200905_1811	2020-09-05 21:11:59.487063+03
39	base	0024_staticdata	2020-09-08 11:46:15.740462+03
40	base	0025_insert_static_data	2020-09-08 11:55:19.998303+03
41	base	0024_auto_20201130_0842	2020-11-30 11:44:29.961796+03
42	base	0025_auto_20201130_1040	2020-11-30 13:40:25.668003+03
43	base	0026_auto_20201130_2147	2020-12-01 00:47:27.392834+03
44	base	0027_auto_20201207_1310	2020-12-07 16:10:17.04331+03
45	base	0028_auto_20210104_0441	2021-01-04 07:41:41.083588+03
46	base	0029_auto_20210104_0441	2021-01-04 07:41:41.272044+03
47	base	0030_auto_20210112_2134	2021-01-13 00:34:20.535495+03
48	base	0031_alertslog_payment	2021-01-13 00:36:54.588911+03
49	base	0032_traininggroup_available_for_additional_lessons	2021-01-19 20:08:57.330082+03
50	base	0033_grouptrainingday_pay_visitors	2021-01-20 23:17:15.370048+03
51	base	0034_staticdata_tarif_payment_add_lesson	2021-01-20 23:17:45.613538+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
s3aitm0xnwwikvr16cuktaijqjhk2edy	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-07-29 15:19:08.352119+03
8ktuy9yxalki32v82vcu9dmwohpbbxtk	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-07-30 14:41:43.897008+03
s6q2v30gi6kj93qt5wzzvqb83bqdpq5v	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-08-13 16:03:28.415883+03
dc4v7utbki9qcs1sn53px0q3xya0b3n3	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-08-25 10:51:52.024718+03
klrcoe4xf13twy1jsibo5h436xxmofdj	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-08-26 13:58:38.238703+03
sif3u85oimqolaskc68wdyjvc3do9ip9	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-08-26 21:58:49.188548+03
uo2e59atd7b9w41ntd01svegfcil1mzc	NmJiYzA4ZjYzOTkxZWMxODJhNjk4M2RiZWViZjI4ZDAzOTg1ZjMwZDp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjEwYzllNjZhYjFiMjlhMzUzMDk5NzNlZDY1MGI0OGRiNTRmNzYxNGUifQ==	2020-08-27 02:36:48.80777+03
cegg3ciz6v22g84y50e70lccdkx8tyyk	NmJiYzA4ZjYzOTkxZWMxODJhNjk4M2RiZWViZjI4ZDAzOTg1ZjMwZDp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjEwYzllNjZhYjFiMjlhMzUzMDk5NzNlZDY1MGI0OGRiNTRmNzYxNGUifQ==	2020-08-28 17:53:45.560681+03
u0djcysqhuz41bt7elzdurday15qt3c5	NmJiYzA4ZjYzOTkxZWMxODJhNjk4M2RiZWViZjI4ZDAzOTg1ZjMwZDp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjEwYzllNjZhYjFiMjlhMzUzMDk5NzNlZDY1MGI0OGRiNTRmNzYxNGUifQ==	2020-08-29 21:58:11.4818+03
dqpsjighlbs48jrq30n6eo91e1zrke9n	ZDhhNWI2YTI0NWFjYTJkOTE3YzQ5NjBlN2MyMTljMzExMTM3ZjMxOTp7Il9hdXRoX3VzZXJfaWQiOiI2MzgzMDMwMDYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJmMDdjODc3OWM3NjllM2QwNTZlM2JjMmNhMmQ4NzQyZWUxMzU3NjQifQ==	2020-08-30 21:16:12.330896+03
wov9rw48x71fy2cb43vd3ptcx5g7jkdk	ZDhhNWI2YTI0NWFjYTJkOTE3YzQ5NjBlN2MyMTljMzExMTM3ZjMxOTp7Il9hdXRoX3VzZXJfaWQiOiI2MzgzMDMwMDYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJmMDdjODc3OWM3NjllM2QwNTZlM2JjMmNhMmQ4NzQyZWUxMzU3NjQifQ==	2020-08-30 21:55:07.281112+03
2n4lc123v0t8o7avf12a2iiwf54ho1pq	ZDhhNWI2YTI0NWFjYTJkOTE3YzQ5NjBlN2MyMTljMzExMTM3ZjMxOTp7Il9hdXRoX3VzZXJfaWQiOiI2MzgzMDMwMDYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJmMDdjODc3OWM3NjllM2QwNTZlM2JjMmNhMmQ4NzQyZWUxMzU3NjQifQ==	2020-08-31 22:53:34.834113+03
soxtrck5lbedezx814y6ibdewiisr6u9	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-09-01 01:11:24.55727+03
c0maiiacaofnww8y2xeqbf69m6mpkl5d	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-09-08 10:40:56.230288+03
eeq0p7a4y43c31o7qa7xyvqdggjlu768	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-09-10 19:30:30.571944+03
i4j1qfp386qf1j3059ebrx7kaoyxzcjk	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-09-18 17:30:59.085676+03
zjxanm89tsakqicrknq1h14df8ykiicu	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-09-27 19:00:38.94489+03
5sw4o3qw3hjiks9abtly1lmbekd5xgkr	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-10-03 13:03:16.556081+03
fgs0ptz804ruyv5s2ppe91m3q9zhac0m	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-10-27 11:53:02.318883+03
e8bdj0e8f5w1que5nbxfcky1ik1o28aw	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-11-14 01:57:04.967167+03
eo13xsg3k23xuhz86pwgweqtqrbwtdsk	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-12-06 18:09:53.097586+03
gsxqng5zk0zc08fbkgtc4qafehu4hlik	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-12-21 16:33:40.562286+03
c0gb8cveu6mnma9030ky61zrc5qjvdh8	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2021-01-05 01:03:29.89269+03
s9bw54qujy4y55ottol5lss1j6rzaqa6	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2021-01-27 01:20:30.688689+03
vxn880ykjv6y3avc4xg9keiv1utw3e6i	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2021-02-17 22:46:33.923833+03
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 39, true);


--
-- Name: base_alertslog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_alertslog_id_seq', 400, true);


--
-- Name: base_channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_channel_id_seq', 1, false);


--
-- Name: base_grouptrainingday_absent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_grouptrainingday_absent_id_seq', 49, true);


--
-- Name: base_grouptrainingday_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_grouptrainingday_id_seq', 966, true);


--
-- Name: base_grouptrainingday_pay_visitors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_grouptrainingday_pay_visitors_id_seq', 15, true);


--
-- Name: base_grouptrainingday_visitors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_grouptrainingday_visitors_id_seq', 81, true);


--
-- Name: base_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_payment_id_seq', 456, true);


--
-- Name: base_staticdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_staticdata_id_seq', 2, true);


--
-- Name: base_traininggroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_traininggroup_id_seq', 8, true);


--
-- Name: base_traininggroup_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_traininggroup_user_id_seq', 55, true);


--
-- Name: base_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_user_groups_id_seq', 1, false);


--
-- Name: base_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.base_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 621, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 51, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: base_alertslog base_alertslog_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_alertslog
    ADD CONSTRAINT base_alertslog_pkey PRIMARY KEY (id);


--
-- Name: base_channel base_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_channel
    ADD CONSTRAINT base_channel_pkey PRIMARY KEY (id);


--
-- Name: base_grouptrainingday_absent base_grouptrainingday_ab_grouptrainingday_id_user_fbe355a0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingday_ab_grouptrainingday_id_user_fbe355a0_uniq UNIQUE (grouptrainingday_id, user_id);


--
-- Name: base_grouptrainingday_absent base_grouptrainingday_absent_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingday_absent_pkey PRIMARY KEY (id);


--
-- Name: base_grouptrainingday_pay_visitors base_grouptrainingday_pa_grouptrainingday_id_user_b1fc9dce_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_pay_visitors
    ADD CONSTRAINT base_grouptrainingday_pa_grouptrainingday_id_user_b1fc9dce_uniq UNIQUE (grouptrainingday_id, user_id);


--
-- Name: base_grouptrainingday_pay_visitors base_grouptrainingday_pay_visitors_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_pay_visitors
    ADD CONSTRAINT base_grouptrainingday_pay_visitors_pkey PRIMARY KEY (id);


--
-- Name: base_grouptrainingday base_grouptrainingday_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday
    ADD CONSTRAINT base_grouptrainingday_pkey PRIMARY KEY (id);


--
-- Name: base_grouptrainingday_visitors base_grouptrainingday_vi_grouptrainingday_id_user_caa8bbcc_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingday_vi_grouptrainingday_id_user_caa8bbcc_uniq UNIQUE (grouptrainingday_id, user_id);


--
-- Name: base_grouptrainingday_visitors base_grouptrainingday_visitors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingday_visitors_pkey PRIMARY KEY (id);


--
-- Name: base_payment base_payment_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_payment
    ADD CONSTRAINT base_payment_pkey PRIMARY KEY (id);


--
-- Name: base_staticdata base_staticdata_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_staticdata
    ADD CONSTRAINT base_staticdata_pkey PRIMARY KEY (id);


--
-- Name: base_traininggroup base_traininggroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_traininggroup
    ADD CONSTRAINT base_traininggroup_pkey PRIMARY KEY (id);


--
-- Name: base_traininggroup_users base_traininggroup_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_user_pkey PRIMARY KEY (id);


--
-- Name: base_traininggroup_users base_traininggroup_user_traininggroup_id_user_id_f4b922a9_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_user_traininggroup_id_user_id_f4b922a9_uniq UNIQUE (traininggroup_id, user_id);


--
-- Name: base_user_groups base_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_pkey PRIMARY KEY (id);


--
-- Name: base_user_groups base_user_groups_user_id_group_id_774631b7_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_user_id_group_id_774631b7_uniq UNIQUE (user_id, group_id);


--
-- Name: base_user base_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user
    ADD CONSTRAINT base_user_pkey PRIMARY KEY (id);


--
-- Name: base_user_user_permissions base_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: base_user_user_permissions base_user_user_permissions_user_id_permission_id_e9093277_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permissions_user_id_permission_id_e9093277_uniq UNIQUE (user_id, permission_id);


--
-- Name: base_user base_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user
    ADD CONSTRAINT base_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: base_alertslog_payment_id_35f8ee25; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_alertslog_payment_id_35f8ee25 ON public.base_alertslog USING btree (payment_id);


--
-- Name: base_alertslog_player_id_a2d4324e; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_alertslog_player_id_a2d4324e ON public.base_alertslog USING btree (player_id);


--
-- Name: base_alertslog_tr_day_id_7ea2943f; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_alertslog_tr_day_id_7ea2943f ON public.base_alertslog USING btree (tr_day_id);


--
-- Name: base_grouptrainingday_absent_grouptrainingday_id_91ce15a9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_grouptrainingday_absent_grouptrainingday_id_91ce15a9 ON public.base_grouptrainingday_absent USING btree (grouptrainingday_id);


--
-- Name: base_grouptrainingday_absent_user_id_44e6519d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_grouptrainingday_absent_user_id_44e6519d ON public.base_grouptrainingday_absent USING btree (user_id);


--
-- Name: base_grouptrainingday_group_id_80910337; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_grouptrainingday_group_id_80910337 ON public.base_grouptrainingday USING btree (group_id);


--
-- Name: base_grouptrainingday_pay_visitors_grouptrainingday_id_1c907f45; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_grouptrainingday_pay_visitors_grouptrainingday_id_1c907f45 ON public.base_grouptrainingday_pay_visitors USING btree (grouptrainingday_id);


--
-- Name: base_grouptrainingday_pay_visitors_user_id_4993ad17; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_grouptrainingday_pay_visitors_user_id_4993ad17 ON public.base_grouptrainingday_pay_visitors USING btree (user_id);


--
-- Name: base_grouptrainingday_visitors_grouptrainingday_id_9d5112bd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_grouptrainingday_visitors_grouptrainingday_id_9d5112bd ON public.base_grouptrainingday_visitors USING btree (grouptrainingday_id);


--
-- Name: base_grouptrainingday_visitors_user_id_9af98114; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_grouptrainingday_visitors_user_id_9af98114 ON public.base_grouptrainingday_visitors USING btree (user_id);


--
-- Name: base_payment_player_id_39b55584; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_payment_player_id_39b55584 ON public.base_payment USING btree (player_id);


--
-- Name: base_traininggroup_user_traininggroup_id_e28016e2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_traininggroup_user_traininggroup_id_e28016e2 ON public.base_traininggroup_users USING btree (traininggroup_id);


--
-- Name: base_traininggroup_user_user_id_6eea575e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_traininggroup_user_user_id_6eea575e ON public.base_traininggroup_users USING btree (user_id);


--
-- Name: base_user_groups_group_id_c0eca7d6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_user_groups_group_id_c0eca7d6 ON public.base_user_groups USING btree (group_id);


--
-- Name: base_user_groups_user_id_29a796b6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_user_groups_user_id_29a796b6 ON public.base_user_groups USING btree (user_id);


--
-- Name: base_user_parent_id_ce524304; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_user_parent_id_ce524304 ON public.base_user USING btree (parent_id);


--
-- Name: base_user_user_permissions_permission_id_0418bc02; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_user_user_permissions_permission_id_0418bc02 ON public.base_user_user_permissions USING btree (permission_id);


--
-- Name: base_user_user_permissions_user_id_2eec4d63; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_user_user_permissions_user_id_2eec4d63 ON public.base_user_user_permissions USING btree (user_id);


--
-- Name: base_user_username_59bfc15c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX base_user_username_59bfc15c_like ON public.base_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_alertslog base_alertslog_payment_id_35f8ee25_fk_base_payment_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_alertslog
    ADD CONSTRAINT base_alertslog_payment_id_35f8ee25_fk_base_payment_id FOREIGN KEY (payment_id) REFERENCES public.base_payment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_alertslog base_alertslog_player_id_a2d4324e_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_alertslog
    ADD CONSTRAINT base_alertslog_player_id_a2d4324e_fk_base_user_id FOREIGN KEY (player_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_alertslog base_alertslog_tr_day_id_7ea2943f_fk_base_grouptrainingday_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_alertslog
    ADD CONSTRAINT base_alertslog_tr_day_id_7ea2943f_fk_base_grouptrainingday_id FOREIGN KEY (tr_day_id) REFERENCES public.base_grouptrainingday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday base_grouptrainingda_group_id_80910337_fk_base_trai; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday
    ADD CONSTRAINT base_grouptrainingda_group_id_80910337_fk_base_trai FOREIGN KEY (group_id) REFERENCES public.base_traininggroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_pay_visitors base_grouptrainingda_grouptrainingday_id_1c907f45_fk_base_grou; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_pay_visitors
    ADD CONSTRAINT base_grouptrainingda_grouptrainingday_id_1c907f45_fk_base_grou FOREIGN KEY (grouptrainingday_id) REFERENCES public.base_grouptrainingday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_absent base_grouptrainingda_grouptrainingday_id_91ce15a9_fk_base_grou; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingda_grouptrainingday_id_91ce15a9_fk_base_grou FOREIGN KEY (grouptrainingday_id) REFERENCES public.base_grouptrainingday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_visitors base_grouptrainingda_grouptrainingday_id_9d5112bd_fk_base_grou; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingda_grouptrainingday_id_9d5112bd_fk_base_grou FOREIGN KEY (grouptrainingday_id) REFERENCES public.base_grouptrainingday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_pay_visitors base_grouptrainingda_user_id_4993ad17_fk_base_user; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_pay_visitors
    ADD CONSTRAINT base_grouptrainingda_user_id_4993ad17_fk_base_user FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_absent base_grouptrainingday_absent_user_id_44e6519d_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingday_absent_user_id_44e6519d_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_visitors base_grouptrainingday_visitors_user_id_9af98114_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingday_visitors_user_id_9af98114_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_payment base_payment_player_id_39b55584_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_payment
    ADD CONSTRAINT base_payment_player_id_39b55584_fk_base_user_id FOREIGN KEY (player_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_traininggroup_users base_traininggroup_u_traininggroup_id_76a0d7bf_fk_base_trai; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_u_traininggroup_id_76a0d7bf_fk_base_trai FOREIGN KEY (traininggroup_id) REFERENCES public.base_traininggroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_traininggroup_users base_traininggroup_users_user_id_a4dc9ccf_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_users_user_id_a4dc9ccf_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_groups base_user_groups_group_id_c0eca7d6_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_group_id_c0eca7d6_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_groups base_user_groups_user_id_29a796b6_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_user_id_29a796b6_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user base_user_parent_id_ce524304_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user
    ADD CONSTRAINT base_user_parent_id_ce524304_fk_base_user_id FOREIGN KEY (parent_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_user_permissions base_user_user_permi_permission_id_0418bc02_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permi_permission_id_0418bc02_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_user_permissions base_user_user_permissions_user_id_2eec4d63_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permissions_user_id_2eec4d63_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

