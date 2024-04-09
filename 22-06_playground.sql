-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 22, 2023 at 10:33 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `playground`
--

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Token', 7, 'add_token'),
(26, 'Can change Token', 7, 'change_token'),
(27, 'Can delete Token', 7, 'delete_token'),
(28, 'Can view Token', 7, 'view_token'),
(29, 'Can add token', 8, 'add_tokenproxy'),
(30, 'Can change token', 8, 'change_tokenproxy'),
(31, 'Can delete token', 8, 'delete_tokenproxy'),
(32, 'Can view token', 8, 'view_tokenproxy'),
(33, 'Can add app_configs', 9, 'add_app_configs'),
(34, 'Can change app_configs', 9, 'change_app_configs'),
(35, 'Can delete app_configs', 9, 'delete_app_configs'),
(36, 'Can view app_configs', 9, 'view_app_configs'),
(37, 'Can add client profile', 10, 'add_clientprofile'),
(38, 'Can change client profile', 10, 'change_clientprofile'),
(39, 'Can delete client profile', 10, 'delete_clientprofile'),
(40, 'Can view client profile', 10, 'view_clientprofile'),
(41, 'Can add transactions', 11, 'add_transactions'),
(42, 'Can change transactions', 11, 'change_transactions'),
(43, 'Can delete transactions', 11, 'delete_transactions'),
(44, 'Can view transactions', 11, 'view_transactions'),
(45, 'Can add token_log', 12, 'add_token_log'),
(46, 'Can change token_log', 12, 'change_token_log'),
(47, 'Can delete token_log', 12, 'delete_token_log'),
(48, 'Can view token_log', 12, 'view_token_log');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$8afrt9I3GqwfurezoXrEnz$oXBL+rOo/fwxLlumZcPoqZ0srlyVB42vjSfJPgg7Gfk=', '2023-06-18 14:15:28.311054', 1, '100000', 'Shiv Enterprise', '', 'rchauhan.iotique@gmail.com', 1, 1, '2023-06-04 07:15:14.000000'),
(31, 'pbkdf2_sha256$600000$WJWmM8WfzpKQeQL3m7iwL5$lO3kl4VE0IuXlRSUjgOS5BlEKRpNyYCdw4VPbJQF6TM=', NULL, 0, '100566', 'Test', '', 'Test@gmail.com', 0, 1, '2023-06-15 07:18:31.372280');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2023-06-11 13:04:36.598136', '27', '100669', 3, '', 4, 1),
(2, '2023-06-11 13:04:36.599060', '28', '100768', 3, '', 4, 1),
(3, '2023-06-11 13:04:36.599655', '29', '100795', 3, '', 4, 1),
(4, '2023-06-11 13:04:36.600934', '30', '768926', 3, '', 4, 1),
(5, '2023-06-11 13:04:59.423178', '100', '100', 1, '[{\"added\": {}}]', 10, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(7, 'authtoken', 'token'),
(8, 'authtoken', 'tokenproxy'),
(5, 'contenttypes', 'contenttype'),
(9, 'playground', 'app_configs'),
(10, 'playground', 'clientprofile'),
(12, 'playground', 'token_log'),
(11, 'playground', 'transactions'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-06-11 13:01:51.404332'),
(2, 'auth', '0001_initial', '2023-06-11 13:01:51.572243'),
(3, 'admin', '0001_initial', '2023-06-11 13:01:51.612713'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-06-11 13:01:51.618515'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-06-11 13:01:51.623111'),
(6, 'contenttypes', '0002_remove_content_type_name', '2023-06-11 13:01:51.644096'),
(7, 'auth', '0002_alter_permission_name_max_length', '2023-06-11 13:01:51.660416'),
(8, 'auth', '0003_alter_user_email_max_length', '2023-06-11 13:01:51.669888'),
(9, 'auth', '0004_alter_user_username_opts', '2023-06-11 13:01:51.674061'),
(10, 'auth', '0005_alter_user_last_login_null', '2023-06-11 13:01:51.684850'),
(11, 'auth', '0006_require_contenttypes_0002', '2023-06-11 13:01:51.685856'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2023-06-11 13:01:51.690881'),
(13, 'auth', '0008_alter_user_username_max_length', '2023-06-11 13:01:51.698029'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2023-06-11 13:01:51.706207'),
(15, 'auth', '0010_alter_group_name_max_length', '2023-06-11 13:01:51.715948'),
(16, 'auth', '0011_update_proxy_permissions', '2023-06-11 13:01:51.720091'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2023-06-11 13:01:51.727631'),
(18, 'authtoken', '0001_initial', '2023-06-11 13:01:51.755775'),
(19, 'authtoken', '0002_auto_20160226_1747', '2023-06-11 13:01:51.770211'),
(20, 'authtoken', '0003_tokenproxy', '2023-06-11 13:01:51.772492'),
(21, 'playground', '0001_initial', '2023-06-11 13:01:51.827079'),
(22, 'sessions', '0001_initial', '2023-06-11 13:01:51.839750'),
(23, 'playground', '0002_token_log', '2023-06-20 15:17:27.433266'),
(24, 'playground', '0003_token_log_encrypted_token', '2023-06-20 15:35:48.033757'),
(25, 'playground', '0004_alter_app_configs_value', '2023-06-21 05:57:56.670346'),
(26, 'playground', '0005_alter_app_configs_value', '2023-06-21 06:27:03.929057');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('slcddjgwdxbomeyzcili12l1yvx24u9h', '.eJxVjEEOwiAQRe_C2hCgM5S4dO8ZyDAwUjU0Ke3KeHdt0oVu_3vvv1Skba1x62WJU1ZnZdXpd0vEj9J2kO_UbrPmua3LlPSu6IN2fZ1zeV4O9--gUq_fms0wOifWUAoCDAIYSraj2JTRD0QCBsCxIU8IwWAAb4CRkxSPKOr9Ad5WN78:1qAtBg:kIm9metY-ilJlcWLaME-Uk3j3iBbtn2iMKr0Z8HGE_4', '2023-07-02 14:15:28.316986');

-- --------------------------------------------------------

--
-- Table structure for table `playground_app_configs`
--

CREATE TABLE `playground_app_configs` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(200) NOT NULL,
  `value` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `playground_app_configs`
--

INSERT INTO `playground_app_configs` (`id`, `name`, `description`, `value`, `created_at`, `updated_at`) VALUES
(1, 'initial_limit', 'initial limit', '50000', '2023-06-15 11:23:24.079258', '2023-06-15 07:17:30.000000'),
(2, 'app_name', 'Application Name', 'Melody', '2023-06-15 07:17:30.000000', '2023-06-15 07:17:30.000000'),
(3, 'canSubAdminCreateUser', 'Can you subadmin create new client acccounts', 'True', '2023-06-15 07:17:30.000000', '2023-06-15 07:17:30.000000'),
(4, 'appMaintananceMode', 'wether the app should be run normally or activate the Maintanance Mode.', 'True', '2023-06-15 07:17:30.000000', '2023-06-15 07:17:30.000000'),
(5, 'api_token', '', 'b\'gAAAAABklAar0q81vG22hetNpK6b9ie7fzvViJzV1M7uwKdcIj0OzY6VPGm3ja2bHpp5DQi2QHB4F47fSAEyvR9gJRMjWofGfV5iqhTQRVYD6EJxyczJsGDqzRHxcWVWasC5GQJFd9c024VEqoj9GjtjvQyw91OzGJHc3V9f5pwmIiN88YuKQerBaMLo34h8QjJdShptQNlgGSdfk6RX0sDgOFhSd7_EGL6COSZYUvrBSiBZ7riik0OImIMIxSRyMFcDKrRYSkmMUP5sOSdMNdaGxBSFTD7F42_yiKIugyt6puravyYQ-5XtXk6zU8iSzuwN7wAW7WGIboUwHAe5GoQXSjgq29F9MXnGbtRlqPD2aqo6B2YGkYOi55jgz2xUbLLRx0FSkyI5Wn2QRggh00LFBhxWLgiV2pr9W8v7NQGP1ihy-nYNOJN8BTInS-Bw-44uynk70SfZhxLWI6gm8rrVWuMOmPGkm000JZQmZCmN0bFq4fuBhE8d6KZNh6NxqhCUVGQhKAqfQDN5z1X_I5KeDvc6bjSr3z9cj53eh3V--NFugu0ahF8JONl7s5OrDbbfMMsfueUn\'', '2023-06-15 07:17:30.000000', '2023-06-22 08:30:35.287584');

-- --------------------------------------------------------

--
-- Table structure for table `playground_clientprofile`
--

CREATE TABLE `playground_clientprofile` (
  `client_id` varchar(100) NOT NULL,
  `limit` int(11) NOT NULL,
  `phone` varchar(12) DEFAULT NULL,
  `note` varchar(100) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `playground_clientprofile`
--

INSERT INTO `playground_clientprofile` (`client_id`, `limit`, `phone`, `note`, `user_id`) VALUES
('100', 999908170, '123123', '123123', 1),
('566', 50000, '123123', NULL, 31);

-- --------------------------------------------------------

--
-- Table structure for table `playground_token_log`
--

CREATE TABLE `playground_token_log` (
  `id` int(11) NOT NULL,
  `request_url` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `encrypted_token` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `playground_token_log`
--

INSERT INTO `playground_token_log` (`id`, `request_url`, `created_at`, `encrypted_token`) VALUES
(1, 'qfJ4CzlZKRXkOgggKWPT-98CZrKzc1w-HZalzn6IwMce3akeEosqJm6Zz45rIGUGtDWpWSo7_vA=', '2023-06-20 15:39:08.228972', 'b\'4LUVbH4wQQzPGBIkKAnx2us3b4D0L20NS7-M2z-35d5RovJTUet3eKn6ogX32FpGiLepsFU7c7Y\''),
(2, 'qfJ4CzlZKRXkOgggKWPT-98CZrKzc1w-HZalzn6IwMce3akeEosqJm6Zz45rIGUGtDWpWSo7_vA=', '2023-06-20 15:46:57.300580', 'b\'4LUVbH4wQQzPGBIkKAnx2us3b4D0L20NS7-M2z-35d5RovJTUet3eKn6ogX32FpGiLepsFU7c7Y\''),
(3, 'qfJ4CzlZKRXkOgggKWPT-98CZrKzc1w-HZalzn6IwMce3akeEosqJm6Zz45rIGUGtDWpWSo7_vA=', '2023-06-20 15:52:50.589046', 'b\'4LUVbH4wQQzPGBIkKAnx2us3b4D0L20NS7-M2z-35d5RovJTUet3eKn6ogX32FpGiLepsFU7c7Y\''),
(4, 'qfJ4CzlZKRXkOgggKWPT-98CZrKzc1w-HZalzn6IwMce3akeEosqJm6Zz45rIGUGtDWpWSo7_vA=', '2023-06-21 05:39:19.804581', 'b\'4LUVbH4wQQzPGBIkKAnx2us3b4D0L20NS7-M2z-35d5RovJTUet3eKn6ogX32FpGiLepsFU7c7Y\''),
(5, 'vtdgBn93RBrXPixDLxHliNVRcIu2THl6TJi53Enr7P8e3akeEosqJhK01zcSUjdI7IaMMc_OSXY=', '2023-06-21 05:41:25.377126', 'b\'4LUVbH4wQQzYPQopbiec1dgzS-PyXVt-Qeya4jqIwJoArO5BZohbQC5URZzu-rP09bH701N8Z_w\''),
(6, 'vtdgBn93RBrXPixDLxHliNVRcIu2THl6TJi53Enr7P8e3akeEosqJhK01zcSUjdI7IaMMc_OSXY=', '2023-06-21 05:43:24.173926', 'b\'4LUVbH4wQQzYPQopbiec1dgzS-PyXVt-Qeya4jqIwJoArO5BZohbQC5URZzu-rP09bH701N8Z_w\''),
(7, 'vtdgBn93RBrXPixDLxHliNVRcIu2THl6TJi53Enr7P8e3akeEosqJhK01zcSUjdI7IaMMc_OSXY=', '2023-06-21 05:43:56.737990', 'b\'4LUVbH4wQQzYPQopbiec1dgzS-PyXVt-Qeya4jqIwJoArO5BZohbQC5URZzu-rP09bH701N8Z_w\''),
(8, 'vtdgBn93RBrXPixDLxHliNVRcIu2THl6TJi53Enr7P8e3akeEosqJhK01zcSUjdI7IaMMc_OSXY=', '2023-06-21 05:44:24.179987', 'b\'4LUVbH4wQQzYPQopbiec1dgzS-PyXVt-Qeya4jqIwJoArO5BZohbQC5URZzu-rP09bH701N8Z_w\''),
(9, 'vtdgBn93RBrXPixDLxHliNVRcIu2THl6TJi53Enr7P8e3akeEosqJhK01zcSUjdI7IaMMc_OSXY=', '2023-06-21 05:44:45.979254', 'b\'4LUVbH4wQQzYPQopbiec1dgzS-PyXVt-Qeya4jqIwJoArO5BZohbQC5URZzu-rP09bH701N8Z_w\''),
(10, 'o8N6aCNWOjTxHAIGaDD48dcgQ4WwfFUmQumC-DWZ1PEe3akeEosqJiUGTMpCZTZ-vGRfXOKLDMs=', '2023-06-21 05:54:28.185811', 'b\'4LUVbH4wQQzFKRBHMgbi-_4RZaa1fEYHQ52p7Dy47MYO3dVlGvpjTjuN8WgKYANPHcN0Jk1AIOo\''),
(11, 'o8N6aCNWOjTxHAIGaDD48dcgQ4WwfFUmQumC-DWZ1PEe3akeEosqJiUGTMpCZTZ-vGRfXOKLDMs=', '2023-06-21 05:54:53.666281', 'b\'4LUVbH4wQQzFKRBHMgbi-_4RZaa1fEYHQ52p7Dy47MYO3dVlGvpjTjuN8WgKYANPHcN0Jk1AIOo\''),
(12, 'vdlEKiVKRUjNGD8EDjDe-9IhFYL4cX4_dJeB7HWWneYe3akeEosqJkxh4ckq9uOOb405I_jr2oI=', '2023-06-21 05:55:58.208274', 'b\'4LUVbH4wQQzbMy4FNBqdh8IVWKTTfGANRpz_63S1x984o9ZxWvUqWcc8pOO7juWe1X8I-zApB6I\''),
(13, 'sOt_GCJWJ0nWLxdDZCHs9YwDYOTtKUIoWO673jvuzcoe3akeEosqJouBRYoAkPQ-A2MxVD2Ua-c=', '2023-06-21 05:57:14.962932', 'b\'4LUVbH4wQQzWARU3Mwb_htkicOO5bVIDGL6KjWHt-8gU2uxDFI16df43XvO2pd8JrsPXSrInCHQ\''),
(14, 'sO5NGStnJkjSAgUFChHDxfUdauf0cXYEGZSv_3uj98Ae3akeEosqJkwgaPQvNpFkVxOZKFeaKbc=', '2023-06-21 05:59:09.783632', 'b\'4LUVbH4wQQzWBCc2Ojf-h90PYqXXXX0zYaCAjni1z-RVoPhiVMBAf20lVNSuKUTv1pHICdyZ2y8\''),
(15, 'uuldFQNZEgTbOjUbKBHg9NlREanUc0c9bJClwGC26fse3akeEosqJmn0M6aMAbVAYORuriOkOp0=', '2023-06-22 08:30:33.183583', 'b\'4LUVbH4wQQzcAzc6EgnKy9Q3Urv1XV4CTez7wFi3_t0gpPJdT9VeRJxva5A3XZjm5TIiT3MR_EQ\'');

-- --------------------------------------------------------

--
-- Table structure for table `playground_transactions`
--

CREATE TABLE `playground_transactions` (
  `transaction_id` varchar(50) NOT NULL,
  `script_code` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` double NOT NULL,
  `action` varchar(5) NOT NULL,
  `created_by` varchar(50) NOT NULL,
  `updated_by` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `client_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `playground_transactions`
--

INSERT INTO `playground_transactions` (`transaction_id`, `script_code`, `name`, `quantity`, `price`, `action`, `created_by`, `updated_by`, `created_at`, `updated_at`, `client_id`) VALUES
('a02944b0-3e76-4858-9d93-cc185aa2ed1a', 'GOLDMCX', 'Gold Expire 05-Jun', 2, 50, 'Buy', '100', '', '2023-06-11 13:05:28.731266', '2023-06-11 13:05:28.731309', '100'),
('d2bc51a1-a392-4225-a9c5-b3458c2c1606', 'GOLDMCX', 'Gold Expire 05-Jun', 1, 40000, 'Sell', '100', '', '2023-06-11 14:23:47.928409', '2023-06-11 14:23:47.928426', '100'),
('db8b7c75-61b5-4be9-b5cc-911656d3aaa4', 'GOLDMCX', 'Gold Expire 05-Jun', 2, 51780, 'Buy', '100', '', '2023-06-11 14:14:10.866199', '2023-06-11 14:14:10.866215', '100');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `playground_app_configs`
--
ALTER TABLE `playground_app_configs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `playground_clientprofile`
--
ALTER TABLE `playground_clientprofile`
  ADD PRIMARY KEY (`client_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `playground_token_log`
--
ALTER TABLE `playground_token_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `playground_transactions`
--
ALTER TABLE `playground_transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `playground_transacti_client_id_ca8e4b65_fk_playgroun` (`client_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `playground_app_configs`
--
ALTER TABLE `playground_app_configs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `playground_token_log`
--
ALTER TABLE `playground_token_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `playground_clientprofile`
--
ALTER TABLE `playground_clientprofile`
  ADD CONSTRAINT `playground_clientprofile_user_id_00a422cc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `playground_transactions`
--
ALTER TABLE `playground_transactions`
  ADD CONSTRAINT `playground_transacti_client_id_ca8e4b65_fk_playgroun` FOREIGN KEY (`client_id`) REFERENCES `playground_clientprofile` (`client_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
