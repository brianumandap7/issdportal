-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 23, 2025 at 09:02 AM
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
-- Database: `dospms`
--

-- --------------------------------------------------------

--
-- Table structure for table `CBSDeliveryRanking`
--

CREATE TABLE `CBSDeliveryRanking` (
  `id` bigint NOT NULL,
  `PerformanceID` bigint NOT NULL,
  `DepartmentAgencyName` text NOT NULL,
  `AgencyHeadID` bigint NOT NULL,
  `AgencyHeadName` text NOT NULL,
  `RankingRate` double(10,3) NOT NULL,
  `FiscalYear` year NOT NULL,
  `DateStart` date NOT NULL,
  `DateEnds` date NOT NULL,
  `PerformanceDate` date NOT NULL,
  `PerformanceRemarks` text NOT NULL,
  `TransDate` datetime NOT NULL,
  `StatusID` int NOT NULL,
  `StringID` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `CBSDeliveryRankingDetails`
--

CREATE TABLE `CBSDeliveryRankingDetails` (
  `id` bigint NOT NULL,
  `PerformanceID` bigint NOT NULL,
  `FiscalYear` year NOT NULL,
  `DateStart` date NOT NULL,
  `DateEnds` date NOT NULL,
  `RankingID` int NOT NULL COMMENT 'UtilRanking',
  `RankingRate` double(10,3) NOT NULL COMMENT 'Agency Ranking Rate',
  `ServiceMonths` double(10,2) NOT NULL,
  `RatingRank` double(10,3) NOT NULL COMMENT 'Employee Ranking Rate',
  `PlantillaID` bigint NOT NULL,
  `UserID` bigint NOT NULL,
  `LastName` text NOT NULL,
  `EmployeeName` text NOT NULL,
  `DivisionUnitID` bigint NOT NULL,
  `DignatedID` int NOT NULL,
  `PositionID` bigint NOT NULL,
  `OldPositionID` bigint NOT NULL,
  `SGID` bigint NOT NULL,
  `SalaryStepID` bigint NOT NULL,
  `StatusID` bigint NOT NULL,
  `EmployeeStatusID` int NOT NULL,
  `AppointmentID` int NOT NULL,
  `BasicSalary` double(10,2) NOT NULL,
  `PBBAmount` double(10,3) NOT NULL,
  `AssumptionDate` date NOT NULL,
  `ContractDateStart` date NOT NULL,
  `ContractDateEnd` date NOT NULL,
  `OSECNumber` text NOT NULL,
  `ExecutiveOrder` varchar(255) NOT NULL DEFAULT 'Executive Order No. 76 dated 30 April 20',
  `NationalBudgetCircular` varchar(255) NOT NULL DEFAULT 'National Budget Circular No. 540 dated 10 May 2012',
  `DBMCircular` varchar(255) NOT NULL DEFAULT 'DBM Circular No. 2012-20 dated 18 December 2012',
  `ViceID` bigint NOT NULL,
  `WhoID` bigint NOT NULL,
  `ItemNumber` varchar(100) NOT NULL,
  `PageNumber` varchar(100) NOT NULL,
  `CSCBulletin` varchar(200) NOT NULL DEFAULT 'CSCBulletin',
  `CSCDatePublish` date NOT NULL,
  `ShiftID` bigint NOT NULL,
  `Remarks` text NOT NULL,
  `SortMe` int NOT NULL DEFAULT '2',
  `StringID` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `CBSPerformance`
--

CREATE TABLE `CBSPerformance` (
  `id` bigint NOT NULL,
  `PerformanceID` varchar(15) NOT NULL,
  `FiscalYear` year NOT NULL,
  `DateStart` date NOT NULL,
  `DateEnds` date NOT NULL,
  `PerformanceDate` date NOT NULL,
  `RatingPeriod` int NOT NULL,
  `MFOCommonID` bigint NOT NULL,
  `PerformanceTypeID` int NOT NULL,
  `FinalRating` double(10,3) NOT NULL,
  `MotherUnitID` int NOT NULL,
  `DivisionUnitID` int NOT NULL,
  `PositionID` int NOT NULL,
  `RateeID` bigint NOT NULL,
  `RateeLastName` text NOT NULL,
  `RateeName` text NOT NULL,
  `RaterID` bigint NOT NULL,
  `RaterName` text NOT NULL,
  `ApproverID` bigint NOT NULL,
  `ApproverName` text NOT NULL,
  `OfficeHeadID` bigint NOT NULL,
  `OfficeHeadName` text NOT NULL,
  `RaterApproverID` bigint NOT NULL,
  `EncodedID` bigint NOT NULL,
  `CommitmentMessage` text NOT NULL,
  `PerformanceRemarks` text NOT NULL,
  `TransDate` datetime NOT NULL,
  `StatusID` int NOT NULL DEFAULT '1',
  `StringID` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `CBSPerformanceDetails`
--

CREATE TABLE `CBSPerformanceDetails` (
  `id` bigint NOT NULL,
  `MFOID` bigint NOT NULL,
  `GMFOID` bigint NOT NULL,
  `PerformanceID` varchar(15) NOT NULL,
  `GradesTargetsID` bigint NOT NULL,
  `FiscalYear` year NOT NULL,
  `DateStart` date NOT NULL,
  `DateEnds` date NOT NULL,
  `RateeID` bigint NOT NULL,
  `LastName` text NOT NULL,
  `EmployeeName` text NOT NULL,
  `DivisionUnitID` bigint NOT NULL,
  `PositionID` bigint NOT NULL,
  `NumberSorting` double(10,2) NOT NULL,
  `MFOCode` varchar(10) NOT NULL,
  `MajorFinalOutput` text NOT NULL,
  `SuccessIndicators` text NOT NULL COMMENT '(TARGETS + MEASURES)',
  `AllotedBudget` text NOT NULL,
  `IndividualAccountable` text NOT NULL,
  `ActualAccomplishments` text NOT NULL,
  `QualityRating` int NOT NULL,
  `EfficiencyRating` int NOT NULL,
  `TimelinessRating` int NOT NULL,
  `AverageRating` double(10,3) NOT NULL,
  `RemarksRating` text NOT NULL,
  `StatusID` int NOT NULL,
  `TransDate` datetime NOT NULL,
  `NextPageID` int NOT NULL,
  `StringID` varchar(100) NOT NULL,
  `StringGTID` text CHARACTER SET latin1,
  `StringCMID` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `UtilBaseRating`
--

CREATE TABLE `UtilBaseRating` (
  `id` int NOT NULL,
  `NumericalRating` int NOT NULL,
  `AdjectivalRating` varchar(2) NOT NULL,
  `NumRangeFrom` double(5,3) NOT NULL,
  `NumRangeEnd` double(5,3) NOT NULL,
  `PercRangeFrom` varchar(5) NOT NULL,
  `PercRangeEnd` varchar(5) NOT NULL,
  `Description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `UtilBaseRating`
--

INSERT INTO `UtilBaseRating` (`id`, `NumericalRating`, `AdjectivalRating`, `NumRangeFrom`, `NumRangeEnd`, `PercRangeFrom`, `PercRangeEnd`, `Description`) VALUES
(1, 5, 'O', 4.500, 5.000, '130', '999', 'Outstanding: Performance exceeds targets significantly, demonstrating exceptional quality, initiative, and ingenuity.'),
(2, 4, 'VS', 3.500, 4.499, '115', '129', 'Very Satisfactory: Performance exceeds expectations and planned targets.'),
(3, 3, 'S', 2.500, 3.499, '100', '114', 'Satisfactory: Performance meets expectations and achieves planned targets.'),
(4, 2, 'U', 1.500, 2.499, '51', '99', 'Unsatisfactory: Performance fails to meet expectations or falls short of critical goals.'),
(5, 1, 'P', 1.499, 0.000, '50', '00', 'Poor: Performance fails to deliver most targets.');

-- --------------------------------------------------------

--
-- Table structure for table `UtilPerformanceType`
--

CREATE TABLE `UtilPerformanceType` (
  `id` int NOT NULL,
  `PerformanceTypeID` bigint NOT NULL,
  `PerformanceCode` varchar(10) NOT NULL,
  `PerformanceDescription` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `UtilPerformanceType`
--

INSERT INTO `UtilPerformanceType` (`id`, `PerformanceTypeID`, `PerformanceCode`, `PerformanceDescription`) VALUES
(1, 1568178468, 'DPCR', 'Division Performance Commitment Review'),
(2, 1568178548, 'IPCR', 'Individual Performance Commitment Review'),
(3, 1568178388, 'OPCR', 'Office Performance Commitment Review');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `CBSDeliveryRankingDetails`
--
ALTER TABLE `CBSDeliveryRankingDetails`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `CBSPerformance`
--
ALTER TABLE `CBSPerformance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `PerformanceID` (`PerformanceID`);

--
-- Indexes for table `CBSPerformanceDetails`
--
ALTER TABLE `CBSPerformanceDetails`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `MFOID` (`MFOID`);

--
-- Indexes for table `UtilBaseRating`
--
ALTER TABLE `UtilBaseRating`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `UtilPerformanceType`
--
ALTER TABLE `UtilPerformanceType`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `CBSDeliveryRankingDetails`
--
ALTER TABLE `CBSDeliveryRankingDetails`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `CBSPerformance`
--
ALTER TABLE `CBSPerformance`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `CBSPerformanceDetails`
--
ALTER TABLE `CBSPerformanceDetails`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `UtilBaseRating`
--
ALTER TABLE `UtilBaseRating`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `UtilPerformanceType`
--
ALTER TABLE `UtilPerformanceType`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
