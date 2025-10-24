-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 23, 2025 at 08:57 AM
-- Server version: 8.0.42-0ubuntu0.20.04.1
-- PHP Version: 7.4.3-4ubuntu2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dopnpki`
--

-- --------------------------------------------------------

--
-- Table structure for table `Application`
--

CREATE TABLE `Application` (
  `id` int NOT NULL,
  `ApplicationID` varchar(20) NOT NULL,
  `FirstName` varchar(100) NOT NULL,
  `MiddleName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `ExtensionName` varchar(100) NOT NULL,
  `GenderID` int NOT NULL,
  `NationalityID` int DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `TaxIDNumber` varchar(50) NOT NULL,
  `OrgAgencyCompany` varchar(200) NOT NULL,
  `OrgUnitDeptDiv` varchar(200) NOT NULL,
  `HouseUnitNumber` varchar(200) CHARACTER SET utf8mb4 NOT NULL,
  `Street` varchar(200) NOT NULL,
  `Barangay` varchar(50) NOT NULL,
  `MunicipalityCity` varchar(50) NOT NULL,
  `ProvinceState` varchar(50) NOT NULL,
  `ZipCode` varchar(5) NOT NULL,
  `MobileNumber` varchar(50) NOT NULL,
  `EmailAddress` varchar(100) NOT NULL,
  `PassportPhoto` varchar(200) CHARACTER SET utf8mb4 NOT NULL DEFAULT 'passport_photos/avatar_default.jpg',
  `SignatureImage` varchar(200) NOT NULL,
  `TermServiceID` int DEFAULT NULL,
  `StatusID` int DEFAULT NULL,
  `ApplicationDate` date DEFAULT NULL,
  `ApproveDate` date DEFAULT NULL,
  `SubmittedDate` date DEFAULT NULL,
  `TransDate` datetime NOT NULL,
  `StringID` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Application`
--

INSERT INTO `Application` (`id`, `ApplicationID`, `FirstName`, `MiddleName`, `LastName`, `ExtensionName`, `GenderID`, `NationalityID`, `BirthDate`, `TaxIDNumber`, `OrgAgencyCompany`, `OrgUnitDeptDiv`, `HouseUnitNumber`, `Street`, `Barangay`, `MunicipalityCity`, `ProvinceState`, `ZipCode`, `MobileNumber`, `EmailAddress`, `PassportPhoto`, `SignatureImage`, `TermServiceID`, `StatusID`, `ApplicationDate`, `ApproveDate`, `SubmittedDate`, `TransDate`, `StringID`) VALUES
(8, '51Y0EE2XGP8', 'JOSE ANGELO', 'XX', 'BARRANDA', 'JOSE ANGELO BARRANDA', 1, 13, '2025-10-18', '333-333-333-3', 'DDDD', 'DDDD', 'A32', 'UNIT 1502 16 EAST', '030801002', '030801', '0308', '2135', '0432085008', 'JOSEANGELOSBARRANDA@GMAIL.COM', 'passport_photos/eedb711c8ce94c53b8bf17a22f7480b6.jpeg', 'signatures/9ef20fa5871d4fff8d735db2fff47316.png', 1, 2, '2025-10-20', NULL, NULL, '2025-10-20 07:43:18', '83b92a6e5aacdd15a1bb78a5fa94c9fefbb370788fabef813da6a5f0d5644c9b'),
(10, 'BLJ1DGEWJRL', 'JOSE ALEXANDER', 'CULVERA', 'BARRANDA', '', 2, 169, '2025-10-20', '444-444-444', 'fddsf', 'fdsfd', 'fsdf', 'Unit 1502 16 East', '015518020', '015518', '0155', '2135', '0432085008', 'joseangelosbarranda@gmail.com', 'passport_photos/3e81b075b4ed47d49b42f40c4b5953f6.jpg', 'signatures/c85cc62d50d442169010ab1e2e811f49.png', 1, 5, '2025-10-20', '2025-10-20', '2025-10-20', '2025-10-20 15:18:15', '62ed89f407d47a6e75c93c6785864805332560cc13aad76c6d36414cac2ced16'),
(12, 'BLJ1DGEWJRX', 'JOSE ALEXANDER', 'CULVERA', 'BARRANDA', '', 2, 169, '2025-10-20', '444-444-444', 'fddsf', 'fdsfd', 'fsdf', 'Unit 1502 16 East', '015518020', '015518', '0155', '2135', '0432085008', 'joseangelosbarranda@gmail.com', 'passport_photos/3e81b075b4ed47d49b42f40c4b5953f6.jpg', 'signatures/c85cc62d50d442169010ab1e2e811f49.png', 1, 5, '2025-10-20', '2025-10-20', '2025-10-20', '2025-10-20 15:18:15', '62ed89f407d47a6e75c93c6785864805332560cc13aad76c6d36414cac2ced16'),
(13, 'BLJ1DGEWJRS', 'JOSE ALEXANDER', 'CULVERA', 'BARRANDA', '', 2, 169, '2025-10-20', '444-444-444', 'FDDSF', 'FDSFD', 'FSDF', 'UNIT 1502 16 EAST', '015518020', '015518', '0155', '2135', '0432085008', 'JOSEANGELOSBARRANDA@GMAIL.COM', 'passport_photos/3e81b075b4ed47d49b42f40c4b5953f6.jpg', 'signatures/c85cc62d50d442169010ab1e2e811f49.png', 1, 2, '2025-10-20', NULL, NULL, '2025-10-20 15:02:16', '62ed89f407d47a6e75c93c6785864805332560cc13aad76c6d36414cac2ced16'),
(14, '51Y0EE2XGP9', 'JOSE ANGELO', 'XX', 'BARRANDA', 'JOSE ANGELO BARRANDA', 1, 13, '2025-10-18', '333-333-333-3', 'DDDD', 'DDDD', 'A32', 'UNIT 1502 16 EAST', '030801002', '030801', '0308', '2135', '0432085008', 'JOSEANGELOSBARRANDA@GMAIL.COM', 'passport_photos/eedb711c8ce94c53b8bf17a22f7480b6.jpeg', 'signatures/9ef20fa5871d4fff8d735db2fff47316.png', 1, 1, '2025-10-20', NULL, NULL, '2025-10-20 07:43:18', '83b92a6e5aacdd15a1bb78a5fa94c9fefbb370788fabef813da6a5f0d5644c9b'),
(15, 'HRSS6DHXVXY', 'JOSE ANGELO', 'SANOY', 'BARRANDA', '', 1, 169, '2025-10-21', '555-555-555-555', 'DOTR', 'ISSD', '33', 'UNIT 1502 16 EAST', '071218017', '071218', '0712', '2135', '0432085008', 'joseangelobarranda@gmail.com', 'passport_photos/fb8258ebece244cc814da0232a9a80c7.jpg', 'signatures/6067d03ffdc64d61a24f043445b77928.png', 1, 2, '2025-10-21', NULL, NULL, '2025-10-21 13:10:08', '77a8be80c5e5237461ebc5f377f6e1e4f7792f9a96110b724252684189684451');

-- --------------------------------------------------------

--
-- Table structure for table `Attachment`
--

CREATE TABLE `Attachment` (
  `id` int NOT NULL,
  `ApplicationID` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `RequiredID` int NOT NULL,
  `AttachedFiles` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `TransDate` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Attachment`
--

INSERT INTO `Attachment` (`id`, `ApplicationID`, `RequiredID`, `AttachedFiles`, `TransDate`) VALUES
(1, 'XAUFOT4C82U', 1, 'attached_files/IMG_3007_7zcJGeC.PNG', '2025-10-13 06:14:19'),
(2, 'DI8JH3S867U', 1, 'attached_files/IMG_3007_3oGTDiK.PNG', '2025-10-13 06:17:24'),
(3, 'PQYG9JNXNQN', 1, 'attached_files/IMG_3007_GyQE6gw.PNG', '2025-10-13 06:24:30'),
(4, 'WAM1LWFSYSM', 1, 'attached_files/IMG_3007_ZsRTGII.PNG', '2025-10-13 06:44:59'),
(5, 'FMMQHM2NCME', 1, 'attached_files/IMG_3007_GlctJwM.PNG', '2025-10-13 06:45:22'),
(6, '9P5SXBKV0XC', 1, 'attached_files/IMG_3007_jrTTYyF.PNG', '2025-10-13 06:51:28'),
(8, '51Y0EE2XGP8', 4, 'attached_files/d9be847d662a4087bcc5d6292c0146d1.jpg', '2025-10-18 09:32:00'),
(10, 'BLJ1DGEWJRL', 1, 'attached_files/LM_DIEGO_SILANG.jpg', '2025-10-19 23:42:34'),
(12, 'HRSS6DHXVXY', 2, 'attached_files/Flag_of_Caramoan_Camarines_Sur.png', '2025-10-21 02:26:19');

-- --------------------------------------------------------

--
-- Table structure for table `QuarterlyReport`
--

CREATE TABLE `QuarterlyReport` (
  `id` int NOT NULL,
  `QuartID` varchar(20) NOT NULL,
  `Description` varchar(100) NOT NULL,
  `StartsDate` date DEFAULT NULL,
  `EndsDate` date DEFAULT NULL,
  `TransDate` date NOT NULL,
  `StatusID` int NOT NULL,
  `StringID` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `QuarterlyReport`
--

INSERT INTO `QuarterlyReport` (`id`, `QuartID`, `Description`, `StartsDate`, `EndsDate`, `TransDate`, `StatusID`, `StringID`) VALUES
(1, 'E3F6GQ6R0FF', 'FIRST QUARTER 2025', '2025-01-01', '2025-03-31', '2025-10-14', 1, '2217e9ecba522a9d90bbd49af2b77c7afe4885f948efe6ffa9f53961da5e47da'),
(2, 'GLFVF4BHZIW', 'SECOND QUARTER 2025', '2025-04-01', '2025-06-30', '2025-10-14', 1, '28eb443d76dce19847ae84d767197d3a2e93b1715dbe728a1b6fd1cdf8c89f3e'),
(3, '9QKBQANJKDS', 'FOURTH QUARTER 2025', '2025-10-01', '2025-12-31', '2025-10-14', 1, 'c10295cf163ab8172fbe2e5f5fd13362fcbe26a0702a1e109f5a647cc72873ad'),
(4, 'UWA5ECSIUW7', 'THIRD QUARTER 2025', '2025-07-01', '2025-09-30', '2025-10-16', 1, '2eafc2a559b8ad2679580eea0ed1a000b7204f6101038c3bdd8215c3dfca6230');

-- --------------------------------------------------------

--
-- Table structure for table `SummaryReport`
--

CREATE TABLE `SummaryReport` (
  `id` bigint NOT NULL,
  `ReportID` varchar(20) NOT NULL,
  `BatchNumber` varchar(100) NOT NULL,
  `DateStarts` date DEFAULT NULL,
  `DateEnds` date DEFAULT NULL,
  `SubmittedDate` date NOT NULL,
  `ReportRemarks` text NOT NULL,
  `StatusID` int NOT NULL,
  `TransDate` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `SummaryReport`
--

INSERT INTO `SummaryReport` (`id`, `ReportID`, `BatchNumber`, `DateStarts`, `DateEnds`, `SubmittedDate`, `ReportRemarks`, `StatusID`, `TransDate`) VALUES
(1, '8IPWNBSUKX9', '02', '2025-02-01', '2025-02-28', '2025-10-20', 'dasdsadsadsa xxxxx xxASAsasdsadsdsd jasbarrada', 2, '2025-10-20 10:50:53'),
(2, 'QL5WCDC426S', '03', '2025-03-01', '2025-03-31', '2025-10-20', '', 2, '2025-10-20 10:53:26'),
(3, 'I3Q37TL2QZ3', '04', '2025-04-01', '2025-04-30', '2025-10-20', 'XXXXXX', 2, '2025-10-20 10:53:44'),
(5, 'FF3SD130GTP', '01', '2025-01-01', '2025-01-31', '2025-10-21', '', 2, '2025-10-21 07:37:54'),
(6, 'O2B3A3DWUXU', '05', '2025-05-01', '2025-05-31', '2025-10-20', '', 2, '2025-10-20 10:54:11'),
(11, 'RLPAJQ0A5II', '11', '2025-11-01', '2025-11-30', '2025-10-20', '', 2, '2025-10-20 10:56:00'),
(18, 'OCYULB0XHVZ', '07', '2025-07-01', '2025-07-31', '2025-10-20', '', 2, '2025-10-20 10:54:48'),
(19, 'BXKKSX5G28I', '08', '2025-08-01', '2025-08-31', '2025-10-20', '', 2, '2025-10-20 10:55:23'),
(20, 'E411G3DDMYD', '09', '2025-09-01', '2025-09-30', '2025-10-20', '', 2, '2025-10-20 10:55:42'),
(34, '8D8YTQDE161', '06', '2025-06-01', '2025-06-30', '2025-10-20', 'Testing', 2, '2025-10-20 10:54:31'),
(35, '134N42VQIVM', '10', '2025-10-01', '2025-10-31', '2025-10-21', 'None', 2, '2025-10-21 07:38:46'),
(36, '', '12', '2025-12-01', '2025-12-31', '2025-10-20', 'None', 2, '2025-10-20 15:32:45');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Application`
--
ALTER TABLE `Application`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Attachment`
--
ALTER TABLE `Attachment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `QuarterlyReport`
--
ALTER TABLE `QuarterlyReport`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `SummaryReport`
--
ALTER TABLE `SummaryReport`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Application`
--
ALTER TABLE `Application`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `Attachment`
--
ALTER TABLE `Attachment`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `QuarterlyReport`
--
ALTER TABLE `QuarterlyReport`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `SummaryReport`
--
ALTER TABLE `SummaryReport`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
