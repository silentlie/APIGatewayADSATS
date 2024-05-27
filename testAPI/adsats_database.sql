-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2024 at 06:20 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- -----------------------------------------------------
-- Schema adsats_database
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `adsats_database` ;

-- -----------------------------------------------------
-- Schema adsats_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `adsats_database` DEFAULT CHARACTER SET utf8 ;
USE `adsats_database` ;

--
-- Table structure for table `aircrafts`
--

CREATE TABLE `aircrafts` (
  `aircraft_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `aircrafts`
--

INSERT INTO `aircrafts` (`aircraft_id`, `name`, `status`, `start_at`, `end_at`) VALUES
(1, 'AB-CDE', 0, '2022-07-16 00:00:00', '2023-05-01 00:00:00'),
(2, 'KP-SDA', 0, '2022-08-15 00:00:00', NULL),
(3, 'LK-BMA', 0, '2023-04-14 00:00:00', NULL),
(4, 'VP-KJS', 0, '2022-12-05 00:00:00', '2024-03-01 00:00:00'),
(5, 'SJ-ASD', 0, '2023-04-19 00:00:00', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `aircraft_crew`
--

CREATE TABLE `aircraft_crew` (
  `aircraft_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `aircraft_crew`
--

INSERT INTO `aircraft_crew` (`aircraft_id`, `user_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 6),
(1, 12),
(1, 13),
(1, 14),
(1, 20),
(1, 21),
(1, 23),
(1, 24),
(2, 2),
(2, 4),
(2, 6),
(2, 10),
(2, 11),
(2, 13),
(2, 15),
(2, 24),
(3, 2),
(3, 5),
(3, 6),
(3, 7),
(3, 8),
(3, 9),
(3, 10),
(3, 16),
(3, 17),
(3, 23),
(4, 1),
(4, 4),
(4, 5),
(4, 7),
(4, 8),
(4, 12),
(4, 17),
(4, 18),
(4, 19),
(4, 23),
(4, 24),
(4, 25),
(5, 5),
(5, 6),
(5, 7),
(5, 8),
(5, 10),
(5, 17),
(5, 22),
(5, 24);

-- --------------------------------------------------------

--
-- Table structure for table `aircraft_documents`
--

CREATE TABLE `aircraft_documents` (
  `aircrafts_id` int(11) NOT NULL,
  `documents_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `aircraft_documents`
--

INSERT INTO `aircraft_documents` (`aircrafts_id`, `documents_id`) VALUES
(1, 9),
(1, 54),
(1, 83),
(2, 18),
(2, 69),
(3, 11),
(3, 12),
(3, 28),
(3, 37),
(3, 43),
(3, 44),
(3, 54),
(3, 74),
(3, 89),
(3, 95),
(4, 18),
(4, 28),
(4, 36),
(4, 40),
(4, 43),
(4, 45),
(4, 49),
(4, 85),
(4, 89),
(4, 96),
(5, 84),
(5, 89),
(5, 91),
(5, 97);

-- --------------------------------------------------------

--
-- Table structure for table `aircraft_notices`
--

CREATE TABLE `aircraft_notices` (
  `aircraft_id` int(11) NOT NULL,
  `notice_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `aircraft_notices`
--

INSERT INTO `aircraft_notices` (`aircraft_id`, `notice_id`) VALUES
(1, 5),
(1, 6),
(1, 10),
(1, 16),
(1, 34),
(2, 1),
(2, 7),
(2, 17),
(2, 19),
(2, 38),
(3, 6),
(3, 16),
(3, 26),
(3, 27),
(4, 14),
(4, 16),
(4, 31),
(4, 32),
(5, 17),
(5, 33),
(5, 36),
(5, 37);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `name`) VALUES
(1, 'Aircraft'),
(2, 'Audit'),
(3, 'Crew documents'),
(4, 'Purchase order'),
(5, 'Safety management system');

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `document_id` int(11) NOT NULL,
  `uploaded_by_id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `archived` tinyint(4) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `subcategory_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`document_id`, `uploaded_by_id`, `file_name`, `archived`, `created_at`, `modified_at`, `deleted_at`, `subcategory_id`, `user_id`) VALUES
(1, 5, 'Purchase Order #91011.pdf', 0, '2023-08-31 00:00:00', '2024-05-15 00:00:00', NULL, 11, NULL),
(2, 7, 'Aircraft Purchase Agreement.pdf', 0, '2024-03-25 00:00:00', '2024-05-09 00:00:00', NULL, 1, NULL),
(3, 16, 'Regulatory Compliance Report.pdf', 0, '2023-07-31 00:00:00', '2024-02-21 00:00:00', '2024-03-05 00:00:00', 4, NULL),
(4, 2, 'Quality Assurance Audit.pdf', 0, '2024-04-30 00:00:00', '2024-05-14 00:00:00', NULL, 5, NULL),
(5, 8, 'Staff Retention Strategy.xlsx', 0, '2023-11-03 00:00:00', '2024-01-22 00:00:00', NULL, 6, NULL),
(6, 14, 'Purchase Order #272829.pdf', 0, '2024-03-23 00:00:00', '2024-04-29 00:00:00', NULL, 11, NULL),
(7, 17, 'Staff Benefits Package.pdf', 0, '2023-09-25 00:00:00', '2024-04-28 00:00:00', NULL, 15, NULL),
(8, 1, 'Compliance Violation Notice.pdf', 0, '2024-01-20 00:00:00', '2024-05-15 00:00:00', NULL, 3, NULL),
(9, 11, 'Crew Training Program Evaluation.pdf', 0, '2023-08-27 00:00:00', '2023-09-21 00:00:00', NULL, 8, 12),
(10, 24, 'Aircraft Registration.pdf', 1, '2024-04-06 00:00:00', '2024-04-17 00:00:00', NULL, 1, NULL),
(11, 8, 'Aircraft Incident Report.pdf', 0, '2023-12-17 00:00:00', '2024-05-19 00:00:00', NULL, 7, NULL),
(12, 20, 'Safety Compliance Record.docx', 1, '2023-10-02 00:00:00', '2024-01-20 00:00:00', NULL, 10, NULL),
(13, 16, 'Crew Emergency Procedures Manual.xlsx', 1, '2023-08-10 00:00:00', '2023-09-10 00:00:00', NULL, 2, NULL),
(14, 23, 'Staff Recognition Program.pdf', 0, '2024-03-01 00:00:00', '2024-03-01 00:00:00', '2024-03-02 00:00:00', 15, NULL),
(15, 12, 'Crew Medical Certificate.jpg', 1, '2023-09-27 00:00:00', '2024-02-13 00:00:00', NULL, 9, NULL),
(16, 6, 'Staff Diversity Training.docx', 0, '2023-09-19 00:00:00', '2023-09-24 00:00:00', NULL, 15, NULL),
(17, 25, 'Purchase Order #212223.pdf', 0, '2023-08-12 00:00:00', '2023-09-07 00:00:00', '2023-11-13 00:00:00', 11, NULL),
(18, 5, 'Crew Background Check.pdf', 1, '2023-07-06 00:00:00', '2024-03-16 00:00:00', NULL, 15, 18),
(19, 7, 'Purchase Order #454647.pdf', 1, '2024-01-18 00:00:00', '2024-02-01 00:00:00', NULL, 11, NULL),
(20, 1, 'Audit Findings Report.docx', 0, '2023-08-08 00:00:00', '2024-02-07 00:00:00', NULL, 5, NULL),
(21, 9, 'Crew Scheduling System.xlsx', 1, '2024-03-25 00:00:00', '2024-05-07 00:00:00', NULL, 13, NULL),
(22, 24, 'Staff Performance Improvement Plan.xlsx', 1, '2024-02-16 00:00:00', '2024-04-06 00:00:00', NULL, 15, NULL),
(23, 8, 'Purchase Order #303132.xlsx', 1, '2023-09-17 00:00:00', '2023-12-16 00:00:00', NULL, 11, NULL),
(24, 15, 'Maintenance Schedule.docx', 0, '2024-02-21 00:00:00', '2024-04-03 00:00:00', NULL, 1, NULL),
(25, 15, 'Purchase Order #394041.pdf', 0, '2024-03-14 00:00:00', '2024-05-11 00:00:00', NULL, 11, NULL),
(26, 3, 'Crew Performance Management System.xlsx', 0, '2024-05-01 00:00:00', '2024-05-16 00:00:00', NULL, 15, NULL),
(27, 21, 'Safety Audit Report.pdf', 1, '2024-03-10 00:00:00', '2024-05-08 00:00:00', NULL, 5, NULL),
(28, 25, 'Staff Training Certificate.pdf', 0, '2023-12-25 00:00:00', '2024-02-15 00:00:00', NULL, 9, 21),
(29, 11, 'Crew Emergency Procedures Manual.docx', 1, '2023-12-15 00:00:00', '2024-02-14 00:00:00', NULL, 1, NULL),
(30, 1, 'Staff Recognition Program.pdf', 0, '2024-05-21 00:00:00', '2024-05-21 00:00:00', NULL, 15, NULL),
(31, 20, 'Crew Flight Logs.xlsx', 1, '2023-11-30 00:00:00', '2023-12-31 00:00:00', NULL, 7, NULL),
(32, 2, 'Purchase Order #515253.docx', 0, '2023-08-04 00:00:00', '2024-02-19 00:00:00', NULL, 11, NULL),
(33, 11, 'Staff Leave Request.pdf', 0, '2024-03-14 00:00:00', '2024-03-18 00:00:00', '2024-04-18 00:00:00', 15, 17),
(34, 17, 'Purchase Order #515253.pdf', 1, '2023-11-15 00:00:00', '2024-03-08 00:00:00', NULL, 11, NULL),
(35, 10, 'Compliance Policy Manual.xlsx', 1, '2023-12-24 00:00:00', '2024-04-11 00:00:00', NULL, 2, NULL),
(36, 15, 'Regulatory Compliance Training.pdf', 1, '2023-05-29 00:00:00', '2024-05-17 00:00:00', NULL, 8, NULL),
(37, 9, 'Staff Conflict Resolution Training.pdf', 0, '2024-05-10 00:00:00', '2024-05-22 00:00:00', NULL, 15, NULL),
(38, 19, 'Environmental Compliance Report.xlsx', 0, '2023-10-12 00:00:00', '2024-05-10 00:00:00', NULL, 1, NULL),
(39, 1, 'Maintenance Schedule.xlsx', 0, '2023-12-18 00:00:00', '2023-12-30 00:00:00', NULL, 1, NULL),
(40, 8, 'Crew Incident Reporting System.pdf', 0, '2023-11-21 00:00:00', '2023-12-09 00:00:00', NULL, 13, NULL),
(41, 11, 'Staff Performance Improvement Plan.pdf', 1, '2023-08-02 00:00:00', '2024-01-22 00:00:00', NULL, 15, 10),
(42, 7, 'Aircraft Service Record.pdf', 0, '2023-06-26 00:00:00', '2024-04-04 00:00:00', NULL, 1, NULL),
(43, 7, 'Quality Assurance Compliance Report.xlsx', 1, '2023-12-18 00:00:00', '2023-12-28 00:00:00', NULL, 3, NULL),
(44, 5, 'Crew Performance Management System.pdf', 1, '2023-08-25 00:00:00', '2024-04-06 00:00:00', NULL, 15, NULL),
(45, 23, 'Staff Handbook.docx', 1, '2024-05-13 00:00:00', '2024-05-18 00:00:00', NULL, 15, NULL),
(46, 23, 'Staff Handbook.pdf', 1, '2023-11-11 00:00:00', '2024-03-13 00:00:00', NULL, 15, NULL),
(47, 1, 'Quality Assurance Audit.pdf', 0, '2023-06-27 00:00:00', '2023-11-16 00:00:00', NULL, 5, NULL),
(48, 20, 'Crew Training Certificate.pdf', 0, '2023-08-28 00:00:00', '2023-10-28 00:00:00', NULL, 9, 18),
(49, 20, 'Aircraft Maintenance Training Manual.xlsx', 0, '2024-01-30 00:00:00', '2024-03-22 00:00:00', NULL, 2, NULL),
(50, 16, 'Purchase Order #454647.docx', 1, '2023-10-08 00:00:00', '2024-04-10 00:00:00', NULL, 11, NULL),
(51, 9, 'Crew Conflict Resolution Policy.pdf', 1, '2023-07-08 00:00:00', '2024-05-12 00:00:00', NULL, 15, NULL),
(52, 11, 'Safety Audit Report.pdf', 0, '2023-06-07 00:00:00', '2023-09-10 00:00:00', NULL, 5, NULL),
(53, 6, 'Pilot License.pdf', 1, '2023-11-28 00:00:00', '2024-04-14 00:00:00', NULL, 9, 19),
(54, 19, 'Purchase Order #394041.pdf', 1, '2023-06-02 00:00:00', '2024-03-28 00:00:00', NULL, 11, NULL),
(55, 23, 'Aircraft Maintenance Procedure.pdf', 0, '2023-07-20 00:00:00', '2023-09-20 00:00:00', NULL, 1, NULL),
(56, 12, 'Staff Training Certificate.pdf', 1, '2024-01-27 00:00:00', '2024-05-15 00:00:00', NULL, 9, 3),
(57, 8, 'Crew Performance Evaluation Report.pdf', 0, '2024-02-19 00:00:00', '2024-04-19 00:00:00', NULL, 15, 5),
(58, 15, 'Staff Conflict Resolution Workshop.pdf', 0, '2024-02-15 00:00:00', '2024-04-18 00:00:00', NULL, 15, NULL),
(59, 14, 'Compliance Violation Notice.pdf', 1, '2023-07-16 00:00:00', '2024-03-08 00:00:00', NULL, 3, NULL),
(60, 8, 'Aircraft Service Record.docx', 1, '2023-06-03 00:00:00', '2024-04-16 00:00:00', '2024-05-09 00:00:00', 1, NULL),
(61, 19, 'Staff Leave Request.jpg', 1, '2024-05-12 00:00:00', '2024-05-22 00:00:00', '2024-05-23 00:00:00', 15, 6),
(62, 17, 'Purchase Order #151617.xlsx', 0, '2023-11-19 00:00:00', '2023-12-10 00:00:00', NULL, 11, NULL),
(63, 10, 'Crew Training Needs Assessment.pdf', 0, '2023-08-25 00:00:00', '2024-03-31 00:00:00', NULL, 8, 13),
(64, 5, 'Crew Emergency Procedures Manual.pdf', 1, '2023-06-21 00:00:00', '2023-09-02 00:00:00', NULL, 2, NULL),
(65, 17, 'Staff Conflict Resolution Training.pdf', 1, '2023-07-19 00:00:00', '2024-03-18 00:00:00', NULL, 13, NULL),
(66, 24, 'Compliance Checklist.pdf', 1, '2023-07-11 00:00:00', '2024-02-02 00:00:00', NULL, 8, NULL),
(67, 8, 'Quality Control Audit Report.docx', 1, '2023-10-03 00:00:00', '2024-01-26 00:00:00', NULL, 5, NULL),
(68, 11, 'Purchase Order #363738.xlsx', 1, '2023-11-30 00:00:00', '2023-12-20 00:00:00', NULL, 11, NULL),
(69, 10, 'Aircraft Parts Inventory.pdf', 1, '2024-01-10 00:00:00', '2024-05-07 00:00:00', NULL, 11, NULL),
(70, 7, 'Purchase Order #272829.xlsx', 0, '2023-10-22 00:00:00', '2024-01-17 00:00:00', NULL, 11, NULL),
(71, 12, 'Staff Diversity Training.pdf', 0, '2024-05-11 00:00:00', '2024-05-18 00:00:00', NULL, 15, NULL),
(72, 17, 'Safety Compliance Record.xlsx', 0, '2024-03-30 00:00:00', '2024-04-11 00:00:00', NULL, 10, NULL),
(73, 15, 'Crew Training Needs Assessment.xlsx', 0, '2023-09-02 00:00:00', '2024-01-20 00:00:00', NULL, 9, 19),
(74, 4, 'Aircraft Inspection Report.xlsx', 0, '2024-04-01 00:00:00', '2024-04-26 00:00:00', NULL, 1, NULL),
(75, 24, 'Staff Succession Planning.xlsx', 1, '2023-09-16 00:00:00', '2024-03-12 00:00:00', NULL, 15, NULL),
(76, 25, 'Crew Emergency Procedures Manual.xlsx', 0, '2023-07-16 00:00:00', '2023-10-01 00:00:00', NULL, 2, NULL),
(77, 3, 'Safety Compliance Training.pdf', 1, '2023-07-05 00:00:00', '2023-11-01 00:00:00', NULL, 10, NULL),
(78, 18, 'Audit Findings Report.xlsx', 0, '2023-11-29 00:00:00', '2024-03-07 00:00:00', NULL, 5, NULL),
(79, 25, 'Staff Conflict Resolution Workshop.pdf', 0, '2023-08-03 00:00:00', '2023-09-18 00:00:00', '2023-09-27 00:00:00', 15, NULL),
(80, 1, 'Crew Background Check.pdf', 0, '2023-07-17 00:00:00', '2024-05-07 00:00:00', NULL, 15, 5),
(81, 24, 'Aircraft Registration.pdf', 1, '2023-08-26 00:00:00', '2024-04-17 00:00:00', NULL, 1, NULL),
(82, 18, 'Crew Training Program Evaluation.xlsx', 1, '2023-07-09 00:00:00', '2024-02-26 00:00:00', NULL, 8, NULL),
(83, 18, 'Aircraft Incident Reports.pdf', 0, '2023-06-03 00:00:00', '2023-06-08 00:00:00', NULL, 12, NULL),
(84, 2, 'Regulatory Compliance Training.pdf', 0, '2023-07-09 00:00:00', '2023-12-13 00:00:00', NULL, 8, NULL),
(85, 3, 'Aircraft Insurance Policy.pdf', 0, '2023-10-31 00:00:00', '2024-01-05 00:00:00', NULL, 1, NULL),
(86, 4, 'Purchase Order #5678.pdf', 1, '2023-11-13 00:00:00', '2024-02-15 00:00:00', NULL, 11, NULL),
(87, 25, 'Aircraft Inspection Report.pdf', 0, '2024-01-21 00:00:00', '2024-04-22 00:00:00', NULL, 3, NULL),
(88, 25, 'Crew Performance Evaluation Report.pdf', 0, '2024-04-10 00:00:00', '2024-05-11 00:00:00', NULL, 15, 13),
(89, 10, 'Aircraft Safety Compliance Record.pdf', 0, '2023-06-19 00:00:00', '2024-02-03 00:00:00', NULL, 10, NULL),
(90, 5, 'Crew Training Program Evaluation.pdf', 0, '2023-10-03 00:00:00', '2023-12-01 00:00:00', NULL, 8, 17),
(91, 21, 'Crew Scheduling System.docx', 1, '2024-01-30 00:00:00', '2024-05-19 00:00:00', NULL, 15, NULL),
(92, 11, 'Crew Training Evaluation.pdf', 0, '2024-01-25 00:00:00', '2024-03-17 00:00:00', NULL, 9, 11),
(93, 12, 'Purchase Order #424344.pdf', 1, '2023-12-25 00:00:00', '2024-03-18 00:00:00', NULL, 11, NULL),
(94, 13, 'Aircraft Incident Response Plan.pdf', 0, '2024-03-01 00:00:00', '2024-05-16 00:00:00', NULL, 14, NULL),
(95, 14, 'Quality Control Audit Report.pdf', 1, '2024-01-21 00:00:00', '2024-03-03 00:00:00', '2024-04-05 00:00:00', 5, NULL),
(96, 23, 'Aircraft Maintenance Manual.docx', 1, '2023-08-31 00:00:00', '2024-01-18 00:00:00', NULL, 2, NULL),
(97, 15, 'Crew Roster.jpg', 0, '2023-11-07 00:00:00', '2024-04-22 00:00:00', NULL, 15, NULL),
(98, 5, 'Crew Flight Logs.pdf', 1, '2024-02-01 00:00:00', '2024-03-18 00:00:00', NULL, 6, NULL),
(99, 1, 'Purchase Order #1234.docx', 1, '2023-10-29 00:00:00', '2024-01-02 00:00:00', NULL, 11, NULL),
(100, 18, 'Pilot License.jpg', 0, '2024-01-11 00:00:00', '2024-02-05 00:00:00', NULL, 9, 2);

-- --------------------------------------------------------

--
-- Table structure for table `hazard_details`
--

CREATE TABLE `hazard_details` (
  `notice_id` int(11) NOT NULL,
  `description` varchar(3000) DEFAULT NULL,
  `hazard_location` varchar(255) DEFAULT NULL,
  `report_type` varchar(12) DEFAULT NULL,
  `notice_date` date DEFAULT NULL,
  `include_mitigation` tinyint(4) DEFAULT NULL,
  `mitigation_comment` varchar(2000) DEFAULT NULL,
  `likelihood` int(11) DEFAULT NULL,
  `severity` int(11) DEFAULT NULL,
  `risk_severity` varchar(12) DEFAULT NULL,
  `comments` varchar(2000) DEFAULT NULL,
  `review_date` date DEFAULT NULL,
  `review_liklihood` int(11) DEFAULT NULL,
  `review_severity` int(11) DEFAULT NULL,
  `additional_comments` varchar(2000) DEFAULT NULL,
  `register_updated` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `hazard_details`
--

INSERT INTO `hazard_details` (`notice_id`, `description`, `hazard_location`, `report_type`, `notice_date`, `include_mitigation`, `mitigation_comment`, `likelihood`, `severity`, `risk_severity`, `comments`, `review_date`, `review_liklihood`, `review_severity`, `additional_comments`, `register_updated`) VALUES
(1, 'Curabitur nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 'maintenance area', 'Open', '2024-05-12', 0, 'Curabitur nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 2, 2, '4', '', '2024-06-05', 2, 3, 'Emergency response plan needs updating', 1),
(6, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer nec purus vel nisi ultrices ultricies.', 'control tower', 'Confidential', '2023-09-26', 0, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer nec purus vel nisi ultrices ultricies.', 3, 2, '6', 'Note: Pothole in the parking lot', '2023-10-25', 3, 2, 'Hazards are not clearly marked', 1),
(11, 'Phasellus nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 'hangar', 'Open', '2023-08-11', 0, 'Phasellus nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 1, 5, '5', 'keep away from heat sources.', '2023-08-28', 1, 4, 'Safety training is inadequate', 1),
(12, 'Nam nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 'taxiway', 'Confidential', '2023-06-22', 0, 'Nam nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 4, 4, '16', 'Watch out for the loose railing on the stairs.', '2023-07-16', 3, 4, 'Insufficient safety protocols in place', 1),
(19, 'Phasellus nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 'maintenance area', 'Open', '2024-01-03', 1, 'Phasellus nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 3, 5, '15', '', '2024-02-06', 3, 5, 'Insufficient safety protocols in place', 0),
(21, 'Nulla nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 'maintenance area', 'Open', '2024-03-04', 1, 'Nulla nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 4, 5, '20', 'Note: Pothole in the parking lot', '2024-03-19', 4, 5, 'Safety measures need to be improved', 1),
(22, 'Quisque nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 'fueling station', 'Open', '2023-10-02', 0, 'Quisque nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', 2, 2, '4', 'Attention: Faulty light fixture above', '2023-11-18', 2, 3, 'Safety training is inadequate', 1),
(27, 'Lorem ipsum dolor sit amet', 'gate', 'Confidential', '2023-07-01', 1, 'Lorem ipsum dolor sit amet', 5, 3, '25', 'drive slowly.', '2023-08-02', 5, 3, 'Safety equipment is outdated', 1),
(33, 'Proin auctor velit at libero tincidunt', 'baggage handling area', 'Open', '2023-06-07', 0, 'Proin auctor velit at libero tincidunt', 2, 4, '8', '', '2023-07-27', 2, 4, 'Safety training is inadequate', 0);

-- --------------------------------------------------------

--
-- Table structure for table `notices`
--

CREATE TABLE `notices` (
  `notice_id` int(11) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `category` varchar(45) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `resolved` tinyint(4) NOT NULL,
  `created_at` datetime NOT NULL,
  `deadline_at` datetime DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `notices`
--

INSERT INTO `notices` (`notice_id`, `created_by_id`, `category`, `subject`, `resolved`, `created_at`, `deadline_at`, `modified_at`, `deleted_at`) VALUES
(1, 14, 'Hazard report', 'Hazard report: Mold growth detected in the basement', 1, '2024-05-14 00:00:00', '2024-06-13 00:00:00', '2024-05-22 00:00:00', NULL),
(2, 19, 'Notice to crew', 'Crew memo: Reminder to update emergency contact information', 1, '2023-11-05 00:00:00', '2023-12-05 00:00:00', '2023-11-16 00:00:00', NULL),
(3, 3, 'Notice to crew', 'Crew notice: Reminder to wear proper PPE in the construction zone', 1, '2023-06-25 00:00:00', '2023-07-25 00:00:00', '2024-01-06 00:00:00', NULL),
(4, 20, 'Notice to crew', 'Crew memo: Reminder to update emergency contact information', 1, '2023-12-31 00:00:00', '2024-01-30 00:00:00', '2024-04-11 00:00:00', '2024-04-13 00:00:00'),
(5, 5, 'BCAA occurence report', 'Safety alert: Severe weather warning for the area', 1, '2023-11-28 00:00:00', '2023-12-28 00:00:00', '2024-03-18 00:00:00', NULL),
(6, 14, 'Hazard report', 'Urgent: Hazard report in the break room regarding slippery floors', 1, '2023-09-26 00:00:00', '2023-10-26 00:00:00', '2024-04-02 00:00:00', NULL),
(7, 14, 'Notice to crew', 'Crew notification: Safety equipment inventory check', 1, '2023-05-29 00:00:00', '2023-06-28 00:00:00', '2024-04-16 00:00:00', NULL),
(8, 9, 'Notice to crew', 'Urgent notice: Hazardous spill containment measures initiated', 1, '2023-06-20 00:00:00', '2023-07-20 00:00:00', '2024-01-16 00:00:00', NULL),
(9, 13, 'BCAA occurence report', 'Safety notice: Slippery surface warning in the cafeteria', 1, '2024-03-18 00:00:00', '2024-04-17 00:00:00', '2024-05-07 00:00:00', NULL),
(10, 14, 'Notice to crew', 'Crew update: Safety inspection results for the warehouse', 1, '2023-05-28 00:00:00', '2023-06-27 00:00:00', '2023-11-13 00:00:00', NULL),
(11, 23, 'Hazard report', 'Hazard report: Structural damage identified in the building', 1, '2023-08-11 00:00:00', '2023-09-10 00:00:00', '2024-05-08 00:00:00', NULL),
(12, 11, 'Hazard report', 'Hazard report: Biohazard contamination found in the restroom', 1, '2023-06-22 00:00:00', '2023-07-22 00:00:00', '2024-04-21 00:00:00', '2024-04-25 00:00:00'),
(13, 10, 'Notice to crew', 'Crew memo: Reminder to report any safety concerns immediately', 1, '2024-01-24 00:00:00', '2024-02-23 00:00:00', '2024-02-27 00:00:00', NULL),
(14, 7, 'Notice to crew', 'Important alert: Hazardous waste disposal procedures revised', 0, '2024-03-31 00:00:00', '2024-04-30 00:00:00', '2024-05-11 00:00:00', NULL),
(15, 24, 'Notice to crew', 'Crew notification: Scheduled maintenance for fire alarm system', 1, '2023-09-23 00:00:00', '2023-10-23 00:00:00', '2024-03-23 00:00:00', NULL),
(16, 12, 'Safety notice', 'Urgent notice: Hazardous materials spill in the laboratory', 1, '2023-10-15 00:00:00', '2023-11-14 00:00:00', '2024-05-06 00:00:00', NULL),
(17, 19, 'BCAA occurence report', 'Crew notification: Safety equipment inventory check', 1, '2023-11-11 00:00:00', '2023-12-11 00:00:00', '2023-12-09 00:00:00', NULL),
(18, 5, 'Notice to crew', 'Safety reminder: Proper lifting techniques to prevent injuries', 0, '2024-04-30 00:00:00', '2024-05-30 00:00:00', '2024-05-03 00:00:00', '2024-05-03 00:00:00'),
(19, 6, 'Hazard report', 'Hazard report: Mold growth detected in the basement', 0, '2024-01-06 00:00:00', '2024-02-05 00:00:00', '2024-03-31 00:00:00', NULL),
(20, 15, 'BCAA occurence report', 'Safety reminder: Proper lifting techniques to prevent injuries', 1, '2023-10-15 00:00:00', '2023-11-14 00:00:00', '2024-04-22 00:00:00', NULL),
(21, 5, 'Hazard report', 'Urgent notice: Hazardous materials spill in the laboratory', 1, '2024-03-04 00:00:00', '2024-04-03 00:00:00', '2024-05-21 00:00:00', NULL),
(22, 18, 'Hazard report', 'Urgent notice: Hazardous spill containment measures initiated', 1, '2023-10-02 00:00:00', '2023-11-01 00:00:00', '2024-02-14 00:00:00', NULL),
(23, 20, 'BCAA occurence report', 'Safety alert: Severe weather warning for the area', 1, '2023-08-01 00:00:00', '2023-08-31 00:00:00', '2024-05-16 00:00:00', NULL),
(24, 7, 'BCAA occurence report', 'Safety reminder: Proper lifting techniques to prevent injuries', 1, '2024-02-01 00:00:00', '2024-03-02 00:00:00', '2024-04-26 00:00:00', NULL),
(25, 9, 'Notice to crew', 'Crew memo: Reminder to report any safety concerns immediately', 1, '2023-08-29 00:00:00', '2023-09-28 00:00:00', '2024-03-27 00:00:00', NULL),
(26, 4, 'BCAA occurence report', 'Safety notice: Slip and fall prevention tips for the office', 1, '2024-04-17 00:00:00', '2024-05-17 00:00:00', '2024-04-17 00:00:00', NULL),
(27, 2, 'Hazard report', 'Hazard report: Mold growth detected in the basement', 1, '2023-07-05 00:00:00', '2023-08-04 00:00:00', '2024-01-29 00:00:00', NULL),
(28, 17, 'Safety notice', 'Safety notice: Slippery surface warning in the cafeteria', 1, '2023-12-16 00:00:00', '2024-01-15 00:00:00', '2024-03-23 00:00:00', '2024-04-05 00:00:00'),
(29, 18, 'BCAA occurence report', 'Safety alert: Severe weather warning for the area', 1, '2023-07-26 00:00:00', '2023-08-25 00:00:00', '2023-12-29 00:00:00', NULL),
(30, 7, 'Notice to crew', 'Safety briefing: First aid training session announced', 1, '2024-01-24 00:00:00', '2024-02-23 00:00:00', '2024-01-30 00:00:00', NULL),
(31, 19, 'Notice to crew', 'Crew reminder: Lockout/tagout procedures must be followed', 1, '2023-08-17 00:00:00', '2023-09-16 00:00:00', '2024-01-11 00:00:00', NULL),
(32, 8, 'Notice to crew', 'Safety briefing: First aid training session announced', 1, '2023-08-29 00:00:00', '2023-09-28 00:00:00', '2023-09-28 00:00:00', NULL),
(33, 22, 'Hazard report', 'Hazard report: Water leak detected in the storage area', 0, '2023-06-07 00:00:00', '2023-07-07 00:00:00', '2023-11-27 00:00:00', NULL),
(34, 20, 'Safety notice', 'Safety notice: Slippery surface warning in the cafeteria', 1, '2024-05-15 00:00:00', '2024-06-14 00:00:00', '2024-05-20 00:00:00', NULL),
(35, 15, 'Notice to crew', 'Urgent notice: Hazardous spill containment measures initiated', 1, '2023-07-10 00:00:00', '2023-08-09 00:00:00', '2023-09-29 00:00:00', NULL),
(36, 14, 'Safety notice', 'Safety notice: Ergonomic workstation setup guidelines', 1, '2023-07-25 00:00:00', '2023-08-24 00:00:00', '2024-04-24 00:00:00', NULL),
(37, 10, 'Notice to crew', 'Notice to crew: Equipment malfunction reported in the production area', 1, '2023-11-02 00:00:00', '2023-12-02 00:00:00', '2023-11-13 00:00:00', NULL),
(38, 8, 'Notice to crew', 'Important alert: Hazardous waste disposal procedures revised', 1, '2024-02-27 00:00:00', '2024-03-28 00:00:00', '2024-05-21 00:00:00', NULL),
(39, 21, 'Notice to crew', 'Safety reminder: Fire extinguisher inspection scheduled', 1, '2023-11-14 00:00:00', '2023-12-14 00:00:00', '2024-05-13 00:00:00', NULL),
(40, 14, 'Notice to crew', 'Crew notification: Scheduled maintenance for fire alarm system', 1, '2023-12-12 00:00:00', '2024-01-11 00:00:00', '2024-04-16 00:00:00', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `notice_details`
--

CREATE TABLE `notice_details` (
  `notice_id` int(11) NOT NULL,
  `message` varchar(3000) DEFAULT NULL,
  `notice_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `notice_details`
--

INSERT INTO `notice_details` (`notice_id`, `message`, `notice_date`) VALUES
(2, '', '2023-10-24'),
(3, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer nec purus vel nisi ultrices ultricies.', '2023-06-25'),
(4, 'Phasellus nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2023-12-31'),
(7, '', '2023-05-29'),
(8, 'Phasellus nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2023-05-20'),
(10, 'Nulla nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2023-05-28'),
(13, '', '2024-01-24'),
(14, 'Lorem ipsum dolor sit amet', '2024-03-31'),
(15, 'Proin auctor velit at libero tincidunt', '2023-09-23'),
(16, 'Curabitur nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2023-10-15'),
(18, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Integer nec purus vel nisi ultrices ultricies.', '2024-04-27'),
(25, '', '2023-08-29'),
(28, 'Nam nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2023-12-16'),
(30, 'Phasellus nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2024-01-24'),
(31, 'Nulla nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2023-08-17'),
(32, '', '2023-08-14'),
(34, 'Lorem ipsum dolor sit amet', '2024-05-15'),
(35, 'Proin auctor velit at libero tincidunt', '2023-07-10'),
(36, '', '2023-07-03'),
(37, '', '2023-11-02'),
(38, 'Curabitur nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2024-02-27'),
(39, '', '2023-11-14'),
(40, 'Quisque nec justo nec justo ultricies ultricies. Sed nec justo nec justo ultricies ultricies.', '2023-12-12');

-- --------------------------------------------------------

--
-- Table structure for table `notice_documents`
--

CREATE TABLE `notice_documents` (
  `notification_id` int(11) NOT NULL,
  `document_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `notice_documents`
--

INSERT INTO `notice_documents` (`notification_id`, `document_id`) VALUES
(1, 29),
(2, 47),
(4, 46),
(4, 86),
(6, 66),
(7, 28),
(8, 96),
(11, 53),
(13, 12),
(14, 28),
(14, 60),
(14, 77),
(21, 5),
(21, 38),
(25, 20),
(30, 81),
(30, 98),
(32, 100),
(34, 41),
(34, 45),
(34, 88),
(37, 41),
(38, 38),
(39, 25);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `notice_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `read_at` datetime DEFAULT NULL,
  `status` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`notice_id`, `user_id`, `read_at`, `status`) VALUES
(1, 2, NULL, 0),
(1, 3, NULL, 0),
(1, 5, '2024-05-19 00:00:00', 1),
(1, 7, '2024-05-21 00:00:00', 1),
(1, 20, NULL, 0),
(1, 21, NULL, 0),
(1, 24, '2024-05-14 00:00:00', 1),
(1, 25, NULL, 0),
(2, 1, '2023-12-17 00:00:00', 1),
(2, 4, '2023-11-30 00:00:00', 1),
(2, 8, '2023-11-18 00:00:00', 1),
(2, 9, '2023-12-22 00:00:00', 1),
(2, 10, '2023-11-18 00:00:00', 1),
(2, 11, '2023-11-10 00:00:00', 1),
(2, 13, '2024-01-11 00:00:00', 1),
(2, 17, '2024-01-15 00:00:00', 1),
(2, 23, '2023-12-31 00:00:00', 1),
(2, 25, '2023-12-19 00:00:00', 1),
(3, 2, '2023-09-01 00:00:00', 1),
(3, 3, '2023-08-06 00:00:00', 1),
(3, 6, '2023-09-20 00:00:00', 1),
(3, 7, '2023-08-08 00:00:00', 1),
(3, 8, '2023-09-07 00:00:00', 1),
(3, 9, '2023-07-06 00:00:00', 1),
(3, 10, '2023-07-17 00:00:00', 1),
(3, 12, '2023-07-09 00:00:00', 1),
(3, 13, '2023-08-31 00:00:00', 1),
(3, 14, '2023-08-06 00:00:00', 1),
(3, 19, '2023-07-18 00:00:00', 1),
(3, 23, '2023-08-23 00:00:00', 1),
(3, 25, '2023-08-31 00:00:00', 1),
(4, 5, '2024-03-25 00:00:00', 1),
(4, 6, '2024-01-14 00:00:00', 1),
(4, 9, '2024-03-27 00:00:00', 1),
(4, 11, '2024-01-29 00:00:00', 1),
(4, 12, '2024-03-03 00:00:00', 1),
(4, 14, '2024-03-10 00:00:00', 1),
(4, 17, '2024-02-27 00:00:00', 1),
(4, 20, '2024-03-21 00:00:00', 1),
(4, 22, '2024-03-25 00:00:00', 1),
(4, 25, '2024-03-16 00:00:00', 1),
(5, 1, '2024-01-22 00:00:00', 1),
(5, 4, '2024-01-20 00:00:00', 1),
(5, 5, '2024-02-19 00:00:00', 1),
(5, 8, '2023-12-02 00:00:00', 1),
(5, 13, '2023-12-03 00:00:00', 1),
(5, 16, '2023-12-25 00:00:00', 1),
(5, 19, '2023-12-17 00:00:00', 1),
(5, 20, '2024-02-19 00:00:00', 1),
(5, 21, '2024-02-06 00:00:00', 1),
(6, 2, '2023-11-08 00:00:00', 1),
(6, 4, '2023-11-16 00:00:00', 1),
(6, 5, '2023-10-24 00:00:00', 1),
(6, 10, '2023-12-01 00:00:00', 1),
(6, 12, '2023-12-12 00:00:00', 1),
(6, 15, '2023-10-10 00:00:00', 1),
(6, 18, '2023-10-08 00:00:00', 1),
(6, 19, '2023-10-03 00:00:00', 1),
(6, 20, '2023-11-19 00:00:00', 1),
(6, 22, '2023-11-01 00:00:00', 1),
(6, 24, '2023-12-21 00:00:00', 1),
(7, 1, '2023-06-11 00:00:00', 1),
(7, 2, '2023-08-05 00:00:00', 1),
(7, 6, '2023-07-21 00:00:00', 1),
(7, 10, '2023-06-14 00:00:00', 1),
(7, 12, '2023-06-29 00:00:00', 1),
(7, 13, '2023-06-12 00:00:00', 1),
(7, 14, '2023-07-14 00:00:00', 1),
(7, 15, '2023-06-30 00:00:00', 1),
(7, 17, '2023-06-08 00:00:00', 1),
(7, 21, '2023-08-17 00:00:00', 1),
(7, 22, '2023-06-06 00:00:00', 1),
(8, 2, '2023-07-24 00:00:00', 1),
(8, 4, '2023-08-17 00:00:00', 1),
(8, 6, '2023-06-24 00:00:00', 1),
(8, 7, '2023-09-14 00:00:00', 1),
(8, 8, '2023-08-18 00:00:00', 1),
(8, 9, '2023-08-02 00:00:00', 1),
(8, 11, '2023-06-24 00:00:00', 1),
(8, 13, '2023-07-21 00:00:00', 1),
(8, 15, '2023-07-25 00:00:00', 1),
(8, 16, '2023-08-03 00:00:00', 1),
(8, 21, '2023-07-23 00:00:00', 1),
(8, 22, '2023-08-23 00:00:00', 1),
(9, 4, '2024-04-01 00:00:00', 1),
(9, 6, NULL, 0),
(9, 7, NULL, 0),
(9, 8, '2024-04-21 00:00:00', 1),
(9, 10, '2024-03-30 00:00:00', 1),
(9, 11, '2024-05-22 00:00:00', 1),
(9, 12, NULL, 0),
(9, 14, '2024-04-07 00:00:00', 1),
(9, 19, '2024-04-15 00:00:00', 1),
(10, 1, '2023-07-06 00:00:00', 1),
(10, 3, '2023-08-22 00:00:00', 1),
(10, 4, '2023-07-22 00:00:00', 1),
(10, 5, '2023-06-23 00:00:00', 1),
(10, 7, '2023-07-07 00:00:00', 1),
(10, 8, '2023-06-07 00:00:00', 1),
(10, 9, '2023-06-13 00:00:00', 1),
(10, 10, '2023-06-10 00:00:00', 1),
(10, 11, '2023-06-16 00:00:00', 1),
(10, 12, '2023-06-24 00:00:00', 1),
(10, 14, '2023-08-26 00:00:00', 1),
(10, 15, '2023-06-03 00:00:00', 1),
(10, 16, '2023-07-31 00:00:00', 1),
(10, 17, '2023-07-28 00:00:00', 1),
(10, 19, '2023-08-24 00:00:00', 1),
(10, 20, '2023-08-19 00:00:00', 1),
(10, 22, '2023-07-31 00:00:00', 1),
(10, 23, '2023-08-24 00:00:00', 1),
(11, 3, '2023-10-17 00:00:00', 1),
(11, 5, '2023-10-14 00:00:00', 1),
(11, 6, '2023-10-22 00:00:00', 1),
(11, 7, '2023-08-13 00:00:00', 1),
(11, 8, '2023-10-14 00:00:00', 1),
(11, 10, '2023-08-12 00:00:00', 1),
(11, 12, '2023-09-19 00:00:00', 1),
(11, 14, '2023-08-18 00:00:00', 1),
(11, 15, '2023-09-14 00:00:00', 1),
(11, 25, '2023-11-09 00:00:00', 1),
(12, 1, '2023-07-25 00:00:00', 1),
(12, 2, '2023-07-02 00:00:00', 1),
(12, 3, '2023-07-03 00:00:00', 1),
(12, 4, '2023-07-28 00:00:00', 1),
(12, 7, '2023-07-03 00:00:00', 1),
(12, 11, '2023-08-01 00:00:00', 1),
(12, 12, '2023-08-30 00:00:00', 1),
(12, 13, '2023-08-18 00:00:00', 1),
(12, 14, '2023-07-27 00:00:00', 1),
(12, 16, '2023-07-08 00:00:00', 1),
(12, 17, '2023-09-05 00:00:00', 1),
(12, 22, '2023-08-01 00:00:00', 1),
(12, 24, '2023-07-19 00:00:00', 1),
(13, 4, '2024-04-21 00:00:00', 1),
(13, 5, '2024-03-22 00:00:00', 1),
(13, 6, '2024-04-12 00:00:00', 1),
(13, 7, '2024-03-19 00:00:00', 1),
(13, 8, '2024-04-20 00:00:00', 1),
(13, 9, '2024-03-04 00:00:00', 1),
(13, 15, '2024-02-10 00:00:00', 1),
(13, 17, '2024-03-05 00:00:00', 1),
(13, 19, '2024-04-14 00:00:00', 1),
(13, 25, '2024-01-28 00:00:00', 1),
(14, 3, '2024-05-07 00:00:00', 1),
(14, 5, NULL, 0),
(14, 6, '2024-05-19 00:00:00', 1),
(14, 7, NULL, 0),
(14, 8, '2024-05-20 00:00:00', 1),
(14, 11, NULL, 0),
(14, 13, '2024-03-31 00:00:00', 1),
(14, 17, NULL, 0),
(14, 19, '2024-04-12 00:00:00', 1),
(15, 1, '2023-09-29 00:00:00', 1),
(15, 2, '2023-12-21 00:00:00', 1),
(15, 4, '2023-09-26 00:00:00', 1),
(15, 9, '2023-10-25 00:00:00', 1),
(15, 10, '2023-11-23 00:00:00', 1),
(15, 11, '2023-10-21 00:00:00', 1),
(15, 13, '2023-12-11 00:00:00', 1),
(15, 15, '2023-11-07 00:00:00', 1),
(15, 16, '2023-12-08 00:00:00', 1),
(15, 18, '2023-10-29 00:00:00', 1),
(15, 20, '2023-12-02 00:00:00', 1),
(15, 21, '2023-10-01 00:00:00', 1),
(15, 22, '2023-12-18 00:00:00', 1),
(15, 23, '2023-12-13 00:00:00', 1),
(16, 1, '2023-11-07 00:00:00', 1),
(16, 2, '2024-01-09 00:00:00', 1),
(16, 5, '2023-11-19 00:00:00', 1),
(16, 8, '2023-11-30 00:00:00', 1),
(16, 12, '2023-10-20 00:00:00', 1),
(16, 14, '2024-01-10 00:00:00', 1),
(16, 17, '2023-12-05 00:00:00', 1),
(16, 18, '2023-11-02 00:00:00', 1),
(16, 19, '2023-11-22 00:00:00', 1),
(16, 20, '2023-10-27 00:00:00', 1),
(16, 21, '2024-01-10 00:00:00', 1),
(16, 23, '2023-10-21 00:00:00', 1),
(16, 24, '2023-12-15 00:00:00', 1),
(16, 25, '2023-10-24 00:00:00', 1),
(17, 4, '2024-01-27 00:00:00', 1),
(17, 5, '2023-12-14 00:00:00', 1),
(17, 6, '2023-12-13 00:00:00', 1),
(17, 9, '2024-01-19 00:00:00', 1),
(17, 12, '2024-01-20 00:00:00', 1),
(17, 14, '2023-11-19 00:00:00', 1),
(17, 15, '2023-11-13 00:00:00', 1),
(17, 18, '2023-11-29 00:00:00', 1),
(17, 19, '2023-11-12 00:00:00', 1),
(17, 23, '2023-12-24 00:00:00', 1),
(17, 24, '2023-12-10 00:00:00', 1),
(18, 1, NULL, 0),
(18, 2, NULL, 0),
(18, 4, '2024-05-05 00:00:00', 1),
(18, 5, NULL, 0),
(18, 10, NULL, 0),
(18, 11, '2024-05-01 00:00:00', 1),
(18, 13, '2024-05-23 00:00:00', 1),
(18, 14, '2024-05-13 00:00:00', 1),
(18, 15, '2024-05-23 00:00:00', 1),
(18, 16, NULL, 0),
(18, 23, NULL, 0),
(19, 4, '2024-01-18 00:00:00', 1),
(19, 5, '2024-01-23 00:00:00', 1),
(19, 14, '2024-01-19 00:00:00', 1),
(19, 15, '2024-03-13 00:00:00', 1),
(19, 18, '2024-02-21 00:00:00', 1),
(19, 19, '2024-03-30 00:00:00', 1),
(19, 20, '2024-03-08 00:00:00', 1),
(19, 25, '2024-01-24 00:00:00', 1),
(20, 2, '2023-11-07 00:00:00', 1),
(20, 5, '2024-01-07 00:00:00', 1),
(20, 6, '2023-12-16 00:00:00', 1),
(20, 12, '2023-12-12 00:00:00', 1),
(20, 13, '2023-10-21 00:00:00', 1),
(20, 18, '2023-10-18 00:00:00', 1),
(20, 22, '2023-10-21 00:00:00', 1),
(20, 23, '2024-01-01 00:00:00', 1),
(20, 24, '2023-11-01 00:00:00', 1),
(21, 1, NULL, 0),
(21, 2, NULL, 0),
(21, 3, NULL, 0),
(21, 6, NULL, 0),
(21, 9, '2024-05-09 00:00:00', 1),
(21, 12, NULL, 0),
(21, 16, '2024-03-13 00:00:00', 1),
(21, 18, NULL, 0),
(21, 19, '2024-03-04 00:00:00', 1),
(21, 20, '2024-05-19 00:00:00', 1),
(21, 21, NULL, 0),
(21, 22, '2024-03-23 00:00:00', 1),
(21, 23, '2024-03-07 00:00:00', 1),
(22, 3, '2023-12-14 00:00:00', 1),
(22, 4, '2023-12-23 00:00:00', 1),
(22, 9, '2023-12-24 00:00:00', 1),
(22, 11, '2023-11-14 00:00:00', 1),
(22, 15, '2023-11-01 00:00:00', 1),
(22, 16, '2023-11-19 00:00:00', 1),
(22, 17, '2023-10-05 00:00:00', 1),
(22, 18, '2023-12-31 00:00:00', 1),
(22, 25, '2023-11-15 00:00:00', 1),
(23, 2, '2023-09-03 00:00:00', 1),
(23, 3, '2023-08-13 00:00:00', 1),
(23, 6, '2023-09-16 00:00:00', 1),
(23, 7, '2023-10-17 00:00:00', 1),
(23, 9, '2023-08-04 00:00:00', 1),
(23, 12, '2023-09-17 00:00:00', 1),
(23, 14, '2023-09-26 00:00:00', 1),
(23, 15, '2023-08-04 00:00:00', 1),
(23, 16, '2023-10-30 00:00:00', 1),
(23, 17, '2023-09-20 00:00:00', 1),
(23, 18, '2023-10-25 00:00:00', 1),
(23, 19, '2023-10-29 00:00:00', 1),
(23, 20, '2023-09-06 00:00:00', 1),
(23, 25, '2023-08-26 00:00:00', 1),
(24, 2, '2024-04-19 00:00:00', 1),
(24, 3, '2024-02-17 00:00:00', 1),
(24, 5, '2024-03-30 00:00:00', 1),
(24, 7, '2024-02-19 00:00:00', 1),
(24, 10, '2024-04-25 00:00:00', 1),
(24, 12, '2024-04-18 00:00:00', 1),
(24, 15, '2024-04-29 00:00:00', 1),
(24, 22, '2024-03-19 00:00:00', 1),
(24, 24, '2024-03-02 00:00:00', 1),
(25, 2, '2023-11-22 00:00:00', 1),
(25, 3, '2023-10-21 00:00:00', 1),
(25, 4, '2023-09-20 00:00:00', 1),
(25, 5, '2023-10-15 00:00:00', 1),
(25, 7, '2023-10-15 00:00:00', 1),
(25, 8, '2023-10-15 00:00:00', 1),
(25, 10, '2023-11-14 00:00:00', 1),
(25, 15, '2023-09-23 00:00:00', 1),
(25, 18, '2023-09-26 00:00:00', 1),
(25, 20, '2023-09-27 00:00:00', 1),
(26, 2, '2024-04-27 00:00:00', 1),
(26, 6, '2024-05-19 00:00:00', 1),
(26, 11, '2024-05-11 00:00:00', 1),
(26, 12, NULL, 0),
(26, 16, '2024-04-28 00:00:00', 1),
(26, 18, NULL, 0),
(26, 19, '2024-05-01 00:00:00', 1),
(26, 22, NULL, 0),
(26, 23, '2024-04-27 00:00:00', 1),
(27, 1, '2023-07-27 00:00:00', 1),
(27, 2, '2023-09-22 00:00:00', 1),
(27, 6, '2023-08-12 00:00:00', 1),
(27, 9, '2023-09-03 00:00:00', 1),
(27, 10, '2023-07-13 00:00:00', 1),
(27, 11, '2023-09-06 00:00:00', 1),
(27, 16, '2023-07-09 00:00:00', 1),
(27, 18, '2023-07-22 00:00:00', 1),
(27, 19, '2023-08-05 00:00:00', 1),
(27, 22, '2023-08-18 00:00:00', 1),
(27, 25, '2023-07-19 00:00:00', 1),
(28, 1, '2024-02-24 00:00:00', 1),
(28, 5, '2023-12-31 00:00:00', 1),
(28, 6, '2024-01-18 00:00:00', 1),
(28, 14, '2024-03-03 00:00:00', 1),
(28, 15, '2024-01-27 00:00:00', 1),
(28, 20, '2024-01-01 00:00:00', 1),
(28, 21, '2024-03-09 00:00:00', 1),
(28, 22, '2024-02-25 00:00:00', 1),
(28, 23, '2024-02-18 00:00:00', 1),
(28, 25, '2024-02-14 00:00:00', 1),
(29, 4, '2023-08-19 00:00:00', 1),
(29, 5, '2023-09-23 00:00:00', 1),
(29, 6, '2023-07-27 00:00:00', 1),
(29, 8, '2023-09-07 00:00:00', 1),
(29, 10, '2023-09-19 00:00:00', 1),
(29, 11, '2023-09-14 00:00:00', 1),
(29, 12, '2023-09-28 00:00:00', 1),
(29, 13, '2023-10-11 00:00:00', 1),
(29, 14, '2023-09-05 00:00:00', 1),
(29, 15, '2023-09-25 00:00:00', 1),
(29, 17, '2023-08-17 00:00:00', 1),
(29, 19, '2023-10-04 00:00:00', 1),
(29, 20, '2023-08-27 00:00:00', 1),
(29, 24, '2023-09-21 00:00:00', 1),
(29, 25, '2023-10-08 00:00:00', 1),
(30, 2, '2024-03-21 00:00:00', 1),
(30, 16, '2024-03-23 00:00:00', 1),
(30, 18, '2024-04-01 00:00:00', 1),
(30, 20, '2024-04-15 00:00:00', 1),
(30, 21, '2024-03-31 00:00:00', 1),
(30, 23, '2024-02-25 00:00:00', 1),
(30, 24, '2024-04-12 00:00:00', 1),
(31, 2, '2023-11-12 00:00:00', 1),
(31, 3, '2023-10-21 00:00:00', 1),
(31, 5, '2023-11-13 00:00:00', 1),
(31, 6, '2023-10-21 00:00:00', 1),
(31, 9, '2023-10-04 00:00:00', 1),
(31, 10, '2023-09-08 00:00:00', 1),
(31, 14, '2023-09-03 00:00:00', 1),
(31, 15, '2023-09-21 00:00:00', 1),
(31, 16, '2023-09-25 00:00:00', 1),
(31, 17, '2023-10-16 00:00:00', 1),
(31, 18, '2023-09-16 00:00:00', 1),
(31, 20, '2023-09-20 00:00:00', 1),
(31, 21, '2023-08-20 00:00:00', 1),
(31, 23, '2023-10-31 00:00:00', 1),
(31, 24, '2023-11-04 00:00:00', 1),
(32, 2, '2023-09-08 00:00:00', 1),
(32, 8, '2023-09-03 00:00:00', 1),
(32, 11, '2023-10-28 00:00:00', 1),
(32, 13, '2023-10-02 00:00:00', 1),
(32, 15, '2023-11-16 00:00:00', 1),
(32, 16, '2023-10-10 00:00:00', 1),
(32, 17, '2023-09-30 00:00:00', 1),
(32, 18, '2023-10-21 00:00:00', 1),
(32, 20, '2023-10-14 00:00:00', 1),
(32, 21, '2023-10-03 00:00:00', 1),
(33, 1, '2023-08-17 00:00:00', 1),
(33, 4, '2023-07-12 00:00:00', 1),
(33, 7, '2023-07-28 00:00:00', 1),
(33, 9, '2023-08-05 00:00:00', 1),
(33, 10, '2023-07-20 00:00:00', 1),
(33, 12, '2023-06-24 00:00:00', 1),
(33, 15, '2023-08-20 00:00:00', 1),
(33, 24, '2023-06-24 00:00:00', 1),
(33, 25, '2023-07-03 00:00:00', 1),
(34, 1, '2024-05-23 00:00:00', 1),
(34, 2, NULL, 0),
(34, 4, '2024-06-14 00:00:00', 1),
(34, 5, '2024-07-15 00:00:00', 1),
(34, 6, '2024-05-16 00:00:00', 1),
(34, 7, NULL, 0),
(34, 12, NULL, 0),
(34, 14, '2024-07-07 00:00:00', 1),
(34, 15, '2024-06-09 00:00:00', 1),
(34, 16, NULL, 0),
(34, 17, '2024-05-28 00:00:00', 1),
(34, 18, NULL, 0),
(34, 19, '2024-06-14 00:00:00', 1),
(34, 22, NULL, 0),
(35, 4, '2023-09-05 00:00:00', 1),
(35, 6, '2023-07-19 00:00:00', 1),
(35, 7, '2023-08-07 00:00:00', 1),
(35, 9, '2023-09-26 00:00:00', 1),
(35, 10, '2023-08-04 00:00:00', 1),
(35, 13, '2023-07-29 00:00:00', 1),
(35, 15, '2023-08-16 00:00:00', 1),
(35, 16, '2023-09-23 00:00:00', 1),
(35, 19, '2023-08-20 00:00:00', 1),
(35, 21, '2023-09-21 00:00:00', 1),
(35, 24, '2023-09-26 00:00:00', 1),
(36, 1, '2023-10-20 00:00:00', 1),
(36, 6, '2023-08-26 00:00:00', 1),
(36, 8, '2023-09-01 00:00:00', 1),
(36, 9, '2023-09-03 00:00:00', 1),
(36, 15, '2023-08-15 00:00:00', 1),
(36, 19, '2023-08-18 00:00:00', 1),
(36, 22, '2023-08-15 00:00:00', 1),
(36, 23, '2023-09-02 00:00:00', 1),
(37, 3, '2023-12-09 00:00:00', 1),
(37, 4, '2023-11-14 00:00:00', 1),
(37, 7, '2024-01-12 00:00:00', 1),
(37, 10, '2024-01-21 00:00:00', 1),
(37, 15, '2023-11-16 00:00:00', 1),
(37, 16, '2023-11-29 00:00:00', 1),
(37, 17, '2023-12-04 00:00:00', 1),
(37, 18, '2024-01-26 00:00:00', 1),
(37, 20, '2023-11-23 00:00:00', 1),
(37, 22, '2024-01-19 00:00:00', 1),
(37, 23, '2023-11-13 00:00:00', 1),
(37, 24, '2024-01-26 00:00:00', 1),
(38, 7, '2024-03-16 00:00:00', 1),
(38, 9, NULL, 0),
(38, 10, '2024-03-16 00:00:00', 1),
(38, 13, '2024-03-02 00:00:00', 1),
(38, 15, NULL, 0),
(38, 16, '2024-03-21 00:00:00', 1),
(38, 17, '2024-03-26 00:00:00', 1),
(38, 21, '2024-02-27 00:00:00', 1),
(38, 22, '2024-03-23 00:00:00', 1),
(38, 24, '2024-03-28 00:00:00', 1),
(39, 4, '2023-11-15 00:00:00', 1),
(39, 9, '2024-01-18 00:00:00', 1),
(39, 10, '2024-02-12 00:00:00', 1),
(39, 16, '2023-11-15 00:00:00', 1),
(39, 17, '2023-12-26 00:00:00', 1),
(39, 20, '2024-01-22 00:00:00', 1),
(39, 22, '2024-01-04 00:00:00', 1),
(39, 23, '2023-11-21 00:00:00', 1),
(40, 5, '0000-00-00 00:00:00', 1),
(40, 10, '2023-12-28 00:00:00', 1),
(40, 11, '2024-02-16 00:00:00', 1),
(40, 15, '2024-01-30 00:00:00', 1),
(40, 22, '2024-01-03 00:00:00', 1),
(40, 25, '2024-02-24 00:00:00', 1);

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL,
  `role` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role`, `description`) VALUES
(1, 'administrator', 'the administration of a business, organization, etc.'),
(2, 'cabin attendants', 'The individual that attends to passenger\'s safety and comfort while in flight.'),
(3, 'engineers', 'a person who designs, builds, or maintains engines, machines, or structures'),
(4, 'pilots', 'a person who operates the flying controls of an aircraft.'),
(5, 'safety officer', 'the person who is responsible for the safety of the people who work or visit there.');

-- --------------------------------------------------------

--
-- Table structure for table `subcategories`
--

CREATE TABLE `subcategories` (
  `subcategory_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `subcategories`
--

INSERT INTO `subcategories` (`subcategory_id`, `name`, `description`, `category_id`) VALUES
(1, 'Aircraft approvals, certificates and documents', NULL, 1),
(2, 'Aircraft manuals', NULL, 1),
(3, 'Audit program', NULL, 2),
(4, 'BCAA aircraft occurence reports', NULL, 5),
(5, 'BCAA audits', NULL, 2),
(6, 'Change management', NULL, 5),
(7, 'Fatigue management', NULL, 1),
(8, 'Ground training', NULL, 3),
(9, 'Licence and approvals', NULL, 3),
(10, 'Safety review board', NULL, 5),
(11, 'Purchase orders', NULL, 4),
(12, 'Safety notice', NULL, 5),
(13, 'Notice to crew', NULL, 5),
(14, 'Hazard notice', NULL, 5),
(15, 'HR documents', NULL, 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `f_name` varchar(255) NOT NULL,
  `l_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `avatar_key` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `f_name`, `l_name`, `email`, `status`, `created_at`, `modified_at`, `deleted_at`, `avatar_key`) VALUES
(1, 'Pennie', 'Oxenham', 'poxenham0@huffingtonpost.com', 0, '2024-05-19 00:00:00', '2024-05-21 00:00:00', NULL, NULL),
(2, 'Marie-ann', 'O\'Deoran', 'modeoran1@smugmug.com', 1, '2023-12-10 00:00:00', '2024-01-26 00:00:00', NULL, NULL),
(3, 'Ancell', 'McKeran', 'amckeran2@instagram.com', 1, '2023-11-27 00:00:00', '2024-03-07 00:00:00', NULL, NULL),
(4, 'Ardella', 'Lau', 'alau3@mtv.com', 0, '2023-07-07 00:00:00', '2023-09-29 00:00:00', NULL, NULL),
(5, 'Jaime', 'Amaya', 'jamaya4@ft.com', 1, '2024-04-03 00:00:00', '2024-05-07 00:00:00', NULL, NULL),
(6, 'Jordan', 'Melbury', 'jmelbury5@google.pl', 1, '2023-10-10 00:00:00', '2023-12-03 00:00:00', '2024-05-18 00:00:00', NULL),
(7, 'Genevra', 'Vella', 'gvella6@sciencedirect.com', 0, '2024-01-07 00:00:00', '2024-04-18 00:00:00', NULL, NULL),
(8, 'Kimberley', 'Lenthall', 'klenthall7@360.cn', 1, '2023-07-14 00:00:00', '2023-09-01 00:00:00', NULL, NULL),
(9, 'Caddric', 'de Wilde', 'cdewilde8@oracle.com', 1, '2024-02-12 00:00:00', '2024-03-27 00:00:00', NULL, NULL),
(10, 'Sid', 'Pover', 'spover9@friendfeed.com', 1, '2023-05-26 00:00:00', '2023-10-19 00:00:00', NULL, NULL),
(11, 'Drugi', 'Woodstock', 'dwoodstocka@examiner.com', 0, '2023-11-19 00:00:00', '2023-12-31 00:00:00', NULL, NULL),
(12, 'Yelena', 'Smoughton', 'ysmoughtonb@pinterest.com', 0, '2023-06-28 00:00:00', '2024-03-02 00:00:00', NULL, NULL),
(13, 'Emilia', 'Robiou', 'erobiouc@wiley.com', 0, '2024-02-08 00:00:00', '2024-05-09 00:00:00', '2024-05-19 00:00:00', NULL),
(14, 'Cosette', 'Cocking', 'ccockingd@ask.com', 0, '2023-05-29 00:00:00', '2023-11-09 00:00:00', NULL, NULL),
(15, 'Verena', 'Frill', 'vfrille@networksolutions.com', 1, '2024-03-28 00:00:00', '2024-04-06 00:00:00', NULL, NULL),
(16, 'Mayne', 'Eliot', 'meliotf@qq.com', 0, '2023-11-04 00:00:00', '2024-01-14 00:00:00', NULL, NULL),
(17, 'Karim', 'Tapton', 'ktaptong@gmpg.org', 1, '2024-01-19 00:00:00', '2024-02-29 00:00:00', NULL, NULL),
(18, 'Marj', 'Le Brom', 'mlebromh@wikia.com', 1, '2024-05-07 00:00:00', '2024-05-11 00:00:00', NULL, NULL),
(19, 'Ashton', 'Dalgarnowch', 'adalgarnowchi@cnbc.com', 1, '2024-03-10 00:00:00', '2024-04-02 00:00:00', '2024-05-20 00:00:00', NULL),
(20, 'Lindsay', 'Fosberry', 'lfosberryj@ehow.com', 0, '2023-11-18 00:00:00', '2024-03-21 00:00:00', NULL, NULL),
(21, 'Cathlene', 'Benda', 'cbendak@gizmodo.com', 1, '2023-12-10 00:00:00', '2024-05-01 00:00:00', NULL, NULL),
(22, 'Niles', 'Detloff', 'ndetloffl@slideshare.net', 0, '2024-01-09 00:00:00', '2024-04-28 00:00:00', NULL, NULL),
(23, 'Chaddy', 'Wildin', 'cwildinm@etsy.com', 1, '2023-09-08 00:00:00', '2024-02-15 00:00:00', NULL, NULL),
(24, 'Dulcea', 'Vernham', 'dvernhamn@yellowpages.com', 0, '2023-05-27 00:00:00', '2023-11-26 00:00:00', NULL, NULL),
(25, 'Friedrich', 'O\'Regan', 'foregano@rakuten.co.jp', 0, '2024-02-26 00:00:00', '2024-03-14 00:00:00', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
(1, 3),
(1, 5),
(2, 2),
(3, 2),
(4, 1),
(4, 3),
(4, 5),
(5, 4),
(6, 3),
(7, 4),
(7, 5),
(8, 4),
(9, 4),
(10, 2),
(10, 5),
(11, 4),
(12, 1),
(12, 2),
(13, 4),
(14, 3),
(14, 5),
(15, 2),
(16, 4),
(17, 5),
(18, 4),
(19, 4),
(19, 5),
(20, 3),
(20, 5),
(21, 2),
(22, 4),
(23, 1),
(23, 2),
(24, 4),
(25, 1),
(25, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `aircrafts`
--
ALTER TABLE `aircrafts`
  ADD PRIMARY KEY (`aircraft_id`),
  ADD UNIQUE KEY `id_UNIQUE` (`aircraft_id`),
  ADD UNIQUE KEY `name_UNIQUE` (`name`);

--
-- Indexes for table `aircraft_crew`
--
ALTER TABLE `aircraft_crew`
  ADD PRIMARY KEY (`aircraft_id`,`user_id`),
  ADD KEY `fk_aircraft_crew_users1_idx` (`user_id`) USING BTREE,
  ADD KEY `fk_aircraft_crew_aircrafts1_idx` (`aircraft_id`) USING BTREE;

--
-- Indexes for table `aircraft_documents`
--
ALTER TABLE `aircraft_documents`
  ADD PRIMARY KEY (`aircrafts_id`,`documents_id`),
  ADD KEY `fk_aircraft_documents_documents1_idx` (`documents_id`),
  ADD KEY `fk_aircraft_documents_aircrafts1_idx` (`aircrafts_id`);

--
-- Indexes for table `aircraft_notices`
--
ALTER TABLE `aircraft_notices`
  ADD PRIMARY KEY (`aircraft_id`,`notice_id`),
  ADD KEY `fk_aircraft_notices_notices1_idx` (`notice_id`) USING BTREE,
  ADD KEY `fk_aircraft_notices_aircrafts1_idx` (`aircraft_id`) USING BTREE;

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `id_UNIQUE` (`category_id`),
  ADD UNIQUE KEY `name_UNIQUE` (`name`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`document_id`,`uploaded_by_id`,`subcategory_id`),
  ADD UNIQUE KEY `id_UNIQUE` (`document_id`),
  ADD KEY `fk_documents_users1_idx` (`uploaded_by_id`),
  ADD KEY `fk_documents_users2_idx` (`user_id`),
  ADD KEY `fk_documents_subcategories1_idx` (`subcategory_id`) USING BTREE;

--
-- Indexes for table `hazard_details`
--
ALTER TABLE `hazard_details`
  ADD PRIMARY KEY (`notice_id`),
  ADD KEY `fk_notice_details_notices1_idx` (`notice_id`) USING BTREE;

--
-- Indexes for table `notices`
--
ALTER TABLE `notices`
  ADD PRIMARY KEY (`notice_id`,`created_by_id`),
  ADD UNIQUE KEY `id_UNIQUE` (`notice_id`),
  ADD KEY `fk_notices_users1_idx` (`created_by_id`);

--
-- Indexes for table `notice_details`
--
ALTER TABLE `notice_details`
  ADD PRIMARY KEY (`notice_id`),
  ADD KEY `fk_notice_details_notices1_idx` (`notice_id`) USING BTREE;

--
-- Indexes for table `notice_documents`
--
ALTER TABLE `notice_documents`
  ADD PRIMARY KEY (`notification_id`,`document_id`),
  ADD KEY `fk_notification_documents_documents1_idx` (`document_id`),
  ADD KEY `fk_notification_documents_notifications1_idx` (`notification_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`notice_id`,`user_id`),
  ADD KEY `fk_notifications_users1_idx` (`user_id`),
  ADD KEY `fk_notifications_notices1_idx` (`notice_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`),
  ADD UNIQUE KEY `id_UNIQUE` (`role_id`),
  ADD UNIQUE KEY `role_UNIQUE` (`role`);

--
-- Indexes for table `subcategories`
--
ALTER TABLE `subcategories`
  ADD PRIMARY KEY (`subcategory_id`,`category_id`),
  ADD UNIQUE KEY `id_UNIQUE` (`subcategory_id`),
  ADD KEY `fk_subcategories_categories1_idx` (`category_id`) USING BTREE;

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `id_UNIQUE` (`user_id`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_id`,`role_id`),
  ADD KEY `fk_user_roles_roles1_idx` (`role_id`),
  ADD KEY `fk_user_roles_users1_idx` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `aircrafts`
--
ALTER TABLE `aircrafts`
  MODIFY `aircraft_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `documents`
--
ALTER TABLE `documents`
  MODIFY `document_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `notices`
--
ALTER TABLE `notices`
  MODIFY `notice_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `subcategories`
--
ALTER TABLE `subcategories`
  MODIFY `subcategory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `aircraft_crew`
--
ALTER TABLE `aircraft_crew`
  ADD CONSTRAINT `fk_aircraft_crew_aircrafts1` FOREIGN KEY (`aircraft_id`) REFERENCES `aircrafts` (`aircraft_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_aircraft_crew_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `aircraft_documents`
--
ALTER TABLE `aircraft_documents`
  ADD CONSTRAINT `fk_aircraft_documents_aircrafts1` FOREIGN KEY (`aircrafts_id`) REFERENCES `aircrafts` (`aircraft_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_aircraft_documents_documents1` FOREIGN KEY (`documents_id`) REFERENCES `documents` (`document_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `aircraft_notices`
--
ALTER TABLE `aircraft_notices`
  ADD CONSTRAINT `fk_aircraft_notices_aircrafts1` FOREIGN KEY (`aircraft_id`) REFERENCES `aircrafts` (`aircraft_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_aircrafts_notices_notices1` FOREIGN KEY (`notice_id`) REFERENCES `notices` (`notice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `fk_documents_subcategories1` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategories` (`subcategory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_documents_users1` FOREIGN KEY (`uploaded_by_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_documents_users2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `hazard_details`
--
ALTER TABLE `hazard_details`
  ADD CONSTRAINT `fk_hazard_details_notices1` FOREIGN KEY (`notice_id`) REFERENCES `notices` (`notice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `notices`
--
ALTER TABLE `notices`
  ADD CONSTRAINT `fk_notices_users1` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `notice_details`
--
ALTER TABLE `notice_details`
  ADD CONSTRAINT `fk_notice_details_notices1` FOREIGN KEY (`notice_id`) REFERENCES `notices` (`notice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `notice_documents`
--
ALTER TABLE `notice_documents`
  ADD CONSTRAINT `fk_notification_documents_documents1` FOREIGN KEY (`document_id`) REFERENCES `documents` (`document_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_notification_documents_notifications1` FOREIGN KEY (`notification_id`) REFERENCES `notices` (`notice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `fk_notifications_notices1` FOREIGN KEY (`notice_id`) REFERENCES `notices` (`notice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_notifications_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `subcategories`
--
ALTER TABLE `subcategories`
  ADD CONSTRAINT `fk_subcategories_categories` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD CONSTRAINT `fk_user_roles_roles1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_user_roles_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
