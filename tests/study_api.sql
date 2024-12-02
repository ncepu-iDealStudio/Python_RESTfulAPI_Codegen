/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80402
 Source Host           : localhost:3306
 Source Schema         : study_api

 Target Server Type    : MySQL
 Target Server Version : 80402
 File Encoding         : 65001

 Date: 02/12/2024 14:00:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `adminID` int NULL DEFAULT NULL COMMENT '管理员用户ID',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '对应的用户表ID',
  `departmentID` bigint NULL DEFAULT NULL COMMENT '所属的部门)ID',
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话',
  `officeAddress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '办公地址',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of admin
-- ----------------------------

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `courseID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '课程编号',
  `courseName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '课程名称',
  `teacherID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任课教师编号',
  `count` int NULL DEFAULT NULL COMMENT '可选人数',
  `credit` float NULL DEFAULT NULL COMMENT '学分',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES (1, '1', 'python程序设计', '50501253', 9, 3, 0, '2022-02-15 16:21:13');
INSERT INTO `course` VALUES (2, '00690270', 'C语言程序设计', '50500954', 60, 3, 0, '2022-02-17 12:46:04');
INSERT INTO `course` VALUES (3, '00690160', '软件工程', '50501234', 60, 3.5, 0, '2022-02-17 12:51:21');

-- ----------------------------
-- Table structure for sso_user
-- ----------------------------
DROP TABLE IF EXISTS `sso_user`;
CREATE TABLE `sso_user`  (
  `autoID` bigint NOT NULL AUTO_INCREMENT,
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录账号-默认为手机号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `userType` tinyint(1) NULL DEFAULT NULL COMMENT '账号类型：1--学生；2--老师；3--管理人员',
  `status` tinyint(1) NULL DEFAULT 1 COMMENT '账号的状态：1--可用；0--锁定',
  `isDelete` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 78 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户账号密码登录信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sso_user
-- ----------------------------
INSERT INTO `sso_user` VALUES (11, '1', '5ouDThfwsYpUrCOBaS7j0A==', 'CQvoxBIJYPCoHV8yzJTqh3VBLgQ+tlr/UfWkfpPR3r20NV5YbooZvzkB68A2Nhn3M3OTp0AfAZnrbTn2VZh4DA==', 1, 1, 0, '2022-02-28 11:37:32');
INSERT INTO `sso_user` VALUES (22, '2', 'g1sguMDEWMaL4GrVXLKRgQ==', 'LvoUbw8+yel5G5CKjMEGN3vvVCBPrGPXQIpXBtGdIq5lRkozhBLHV8xzRArSPkBZ6NnmUkl/TWjn5IiGSa9F3g==', 1, 1, 0, '2022-02-28 13:55:28');
INSERT INTO `sso_user` VALUES (33, '3', 'sXQrIa4jsHDLLqT4Gj/unw==', 'fdFPrFytFiprCznMcPcCyWCqWQWQ3lw7LcyZneh6JDajMOJAjwwzsiOlv/1kgRPp8cEXYMvKNaeo/4PPyZRO2Q==', 1, 1, 0, '2022-02-28 13:55:35');
INSERT INTO `sso_user` VALUES (44, '4', 'Z75p+F3I171yT8J8CiAn9A==', 'PzVAh98N2JCKm1RyryE3gfn+TMWriuGz6Db8FUh0QQmcVWx664wR2f5TcfGr3E8nRr7Dj9f389JxBCgfW4Jypw==', 2, 1, 0, '2022-02-28 14:57:28');
INSERT INTO `sso_user` VALUES (55, '5', 'jHIcvfxXgAe4TRz6awHMtA==', 'FmJdJkExpcITQpN5CWHWaifFrOTpbEm0qANmSRC0hanCOLT9Ev6AY4cSXzfLYroNfbYgUmP6Eo9gaK3+0pR1Lg==', 1, 1, 0, '2022-02-28 17:54:52');
INSERT INTO `sso_user` VALUES (66, '6', '95MtNMqVWO99mz88eH8SIA==', 'TYJUxPs3NGrcg43ORs7+ThKoPn0Njxz9+QQdPI2oJFs53danYsqqWOB+pf06Pwmtd1Ktga7Wec6XJ1ktHsJZqQ==', 1, 1, 1, '2022-02-28 17:55:06');
INSERT INTO `sso_user` VALUES (77, '7', 'zYGqDOaw8SrNYU+dJd0KlQ==', 'kDKSuVd51VZ9z8LvLTMPkmt/hBRbuFlN77W6GiHzDvt4wY84/R32obA86uhUWvRxhxWa/59hh0ZFZ1qm3xhdiA==', 2, 1, 1, '2022-02-28 17:57:08');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `studentID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '学号，业务主键',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '对应的用户表ID',
  `classID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '所属班级ID',
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '所属学院',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '学生姓名',
  `agenda` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '性别',
  `age` int NULL DEFAULT NULL COMMENT '年龄',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学生基本信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (1, '120201080430', '2022022811377862', '200001', '527', '张三', '男', 18, NULL, NULL, 0, '2020-09-16 10:58:58');
INSERT INTO `student` VALUES (2, '120201080431', '2022022813559760', '200001', '527', '李四', '男', 19, NULL, NULL, 0, '2020-09-16 10:59:22');
INSERT INTO `student` VALUES (3, '23462327', '2022022813551869', '200002', '527', '翠花', '女', 20, NULL, NULL, 0, '2020-09-18 18:34:19');
INSERT INTO `student` VALUES (4, '23462328', '2022022817542497', '200012', '527', '黑山老妖', '女', 88, NULL, NULL, 0, '2021-05-14 20:30:25');
INSERT INTO `student` VALUES (5, '23461111', '2022022817553278', '2000301', '509', '刘朵朵', '女', 24, NULL, NULL, 0, '2021-05-20 13:25:55');

-- ----------------------------
-- Table structure for student_selected_course
-- ----------------------------
DROP TABLE IF EXISTS `student_selected_course`;
CREATE TABLE `student_selected_course`  (
  `autoID` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `studentID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '学号',
  `courseID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '课程编号',
  `score` int NULL DEFAULT NULL COMMENT '成绩',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学生选课情况基本信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of student_selected_course
-- ----------------------------
INSERT INTO `student_selected_course` VALUES (1, '120201080431', '00690270', 74, '2022-02-17 17:52:44');
INSERT INTO `student_selected_course` VALUES (2, '120201080431', '1', 65, '2022-02-17 17:52:25');
INSERT INTO `student_selected_course` VALUES (3, '23461111', '00690270', 76, '2022-02-17 17:51:39');
INSERT INTO `student_selected_course` VALUES (4, '23461111', '1', 75, '2022-02-17 14:40:07');
INSERT INTO `student_selected_course` VALUES (5, '23462327', '1', 80, '2022-02-17 10:33:41');
INSERT INTO `student_selected_course` VALUES (6, '23462328', '1', 88, '2022-02-17 14:42:44');

-- ----------------------------
-- Table structure for sys_classinfo
-- ----------------------------
DROP TABLE IF EXISTS `sys_classinfo`;
CREATE TABLE `sys_classinfo`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `classID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '班级ID',
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '所属学院',
  `className` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '班级名称',
  `isDeleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否被删除  0 - 未删除  1 - 已删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '班级信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_classinfo
-- ----------------------------
INSERT INTO `sys_classinfo` VALUES (1, '200001', '527', '软件2001班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (2, '200002', '527', '软件2002班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (3, '200011', '527', '计算2001班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (4, '200012', '527', '计算2002班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (5, '2000301', '527', '信安2001班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (6, '2000401', '527', '物联2001班', 0, '2022-02-17 13:31:02');

-- ----------------------------
-- Table structure for sys_collegeinfo
-- ----------------------------
DROP TABLE IF EXISTS `sys_collegeinfo`;
CREATE TABLE `sys_collegeinfo`  (
  `autoID` bigint NOT NULL AUTO_INCREMENT,
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '学院ID编码--业务主键',
  `collegeName` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '学院名称',
  `isDeleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否被删除  0 - 未删除  1 - 已删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学院表，记录学院/系信息，学生-导师-秘书通过学院进行关联' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_collegeinfo
-- ----------------------------
INSERT INTO `sys_collegeinfo` VALUES (1, '527', '控制与计算机工程学院', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (2, '501', '电气与电子工程学院', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (3, '503', '能源动力与机械工程学院', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (4, '504', '经济与管理学院、MBA教育中心', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (5, '505', '新能源学院', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (6, '506', '核科学与工程学院', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (7, '507', '环境科学与工程学院', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (8, '508', '水利与水电工程学院', 0, '2022-02-17 13:31:13');
INSERT INTO `sys_collegeinfo` VALUES (9, '509', '数理学院', 0, '2022-02-17 13:31:13');

-- ----------------------------
-- Table structure for sys_departmentinfo
-- ----------------------------
DROP TABLE IF EXISTS `sys_departmentinfo`;
CREATE TABLE `sys_departmentinfo`  (
  `autoID` bigint NOT NULL AUTO_INCREMENT,
  `departmentID` bigint NULL DEFAULT NULL COMMENT '学院下属的教研室(研究所)ID',
  `parentDepartmentID` bigint NOT NULL DEFAULT 0 COMMENT '父级部门ID',
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '学院ID编码--业务主键',
  `departmentName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '教研室(研究所)名称',
  `departmentType` tinyint(1) NULL DEFAULT 1 COMMENT '部门类型:\r\n1--教研室；\r\n2-研究所；\r\n3 实验中心；\r\n4-办公室；\r\n5-其他',
  `isDeleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否被删除   0 -未被删除  1 - 被删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '教研室与研究所信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_departmentinfo
-- ----------------------------
INSERT INTO `sys_departmentinfo` VALUES (5, 202104280, 2021121142, NULL, '软件教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (6, 202104285, 2021121142, NULL, '控制理论与系统教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (7, 202104286, 2021121142, NULL, '测控技术与仪器教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (8, 202104287, 2021121142, NULL, '控制装置与系统教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (9, 202104288, 2021121142, NULL, '计算机公共基础教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (10, 202104289, 2021121142, NULL, '计算机应用教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (11, 2021042810, 2021121142, NULL, '计算机科学与技术教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (12, 2021042811, 2021121142, NULL, '信息安全教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (13, 2021042812, 0, NULL, '实验中心', 3, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (14, 2021042813, 0, NULL, '研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (15, 2021042814, 2021042813, NULL, '电力大数据研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (16, 2021042815, 0, NULL, '自动控制教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (17, 2021042816, 0, NULL, '测控教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (18, 2021042817, 0, NULL, '计算机教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (22, 2021100821, 0, NULL, '研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (23, 2021100822, 2021100821, NULL, '电磁与超导电工研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (24, 2021100823, 2021100822, NULL, '电力电子网络研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (25, 2021100824, 2021100821, NULL, '电力电子网络研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (26, 2021100825, 2021100821, NULL, '电力市场研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (27, 2021100826, 2021100821, NULL, '电力系统研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (28, 2021100827, 2021100821, NULL, '电工电子教学实验中心', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (29, 2021100828, 2021100821, NULL, '电能转换与节能技术研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (30, 2021100829, 2021100821, NULL, '电网研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (31, 2021100830, 2021100821, NULL, '电子信息技术研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (32, 2021100831, 2021100821, NULL, '高压电与绝缘技术研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (33, 2021100832, 2021100821, NULL, '柔性电力技术研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (34, 2021100833, 2021100821, NULL, '四方研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (35, 2021100834, 2021100821, NULL, '输配电系统研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (36, 2021100835, 2021100821, NULL, '通信技术研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (37, 2021100836, 2021100821, NULL, '现代电子科学技术研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (38, 2021100837, 2021100821, NULL, '新能源电网研究所', 2, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (39, 2021100838, 2021100821, NULL, '新能源电力系统国家重点实验室', 3, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (40, 2021100839, 2021100821, NULL, ' 新能源电力系统国家重点实验室', 3, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (41, 2021100840, 2021100821, NULL, ' 新能源电力系统国家重点实验室', 3, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (42, 2021100841, 0, NULL, ' 新能源电力系统国家重点实验室', 3, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (43, 2021121142, 0, NULL, '教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (44, 2021121343, 2021121142, NULL, '软件工程教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (45, 2021121344, 2021121142, NULL, '机器人与智能系统教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (46, 2021121345, 2021121142, NULL, '计算机教学研究中心', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (47, 2021121346, 2021121142, NULL, '人工智能与物联网工程教研室', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (48, 2022011418328021, 0, NULL, '部门测试1', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (49, 2022011418405703, 0, NULL, '部门测试2', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (50, 2022011418401485, 0, NULL, '部门测试3', 1, 0, '2022-02-17 13:31:28');
INSERT INTO `sys_departmentinfo` VALUES (51, 2022011418409763, 0, NULL, '部门测试_修改', 1, 0, '2022-02-17 13:31:28');

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `teacherID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '教工号',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '对应的用户表ID',
  `departmentID` bigint NULL DEFAULT NULL COMMENT '所属的教研室(研究所)ID',
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话',
  `officeAddress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '办公地址',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '教师信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES (1, '50501253', '2022022814577014', 123, '熊老师', 'wanglaowu@ncepu.edu.cm', '17666668888', '主楼E-706', 0, '2022-02-17 12:57:10');
INSERT INTO `teacher` VALUES (2, '50500954', '2022022817570694', 202104280, '张老师', 'zhang@163.com', '13612344321', '主楼E-708办公室	0', 0, '2022-02-17 12:57:38');

-- ----------------------------
-- Table structure for user_token
-- ----------------------------
DROP TABLE IF EXISTS `user_token`;
CREATE TABLE `user_token`  (
  `autoID` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `userID` bigint UNSIGNED NOT NULL COMMENT '用户id',
  `userType` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '用户类型 0-普通用户； 1-管理员；2-超级管理员',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'token值',
  `expireTime` timestamp NOT NULL COMMENT '超时时间',
  `isValid` tinyint UNSIGNED NOT NULL DEFAULT 1 COMMENT 'token是否可用 1-可用 0-不可用',
  `isDelete` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 72 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'token表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_token
-- ----------------------------
INSERT INTO `user_token` VALUES (5, 2022101215338760, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5NDc4NzUwNywiZXhwIjoxNjk1MTQ3NTA3fQ.eyJpZCI6MjAyMjEwMTIxNTMzODc2MCwidXNlcl90eXBlIjowfQ.Ej2llI4KSXSFnfBRywlHnwTHTQasp7QQ4lZWB_jqQ7CC4gcCdvrED8VfuFimYBgps98rOv3S-2cg2QnDkcAvQw', '2023-09-20 02:18:27', 1, 0, '2022-10-12 15:37:38', '2023-09-15 22:18:27');
INSERT INTO `user_token` VALUES (6, 1, 1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTA2OTQ0MSwiZXhwIjoxNjg1MDczMDQxfQ.eyJpZCI6MSwidXNlcl90eXBlIjoxfQ.QNPTDPJ8GxhLBvFkEh53h22qnIXsgHRa-Jhnreepd4up-mQ7bZu-5CfV4egWdlwUei59i66ea62chtEHSLQKfw', '2023-05-26 11:50:41', 1, 0, '2022-10-12 16:35:32', '2023-05-26 10:50:41');
INSERT INTO `user_token` VALUES (7, 2, 2, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxNzQ4NTY3NCwiZXhwIjoxNzE3ODQ1Njc0fQ.eyJpZCI6MiwidXNlcl90eXBlIjoyfQ.HVI4N3YD9NQWgMSfQvKpYz-1WOEKlJORVFm-Xh63oRiXJJMY2o9xqILd1aJ0nxfyr9mfdUVa2IiH_jm8D3sBTA', '2024-06-08 19:21:14', 1, 0, '2022-10-19 17:19:39', '2024-06-04 07:21:14');
INSERT INTO `user_token` VALUES (8, 3, 1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTg2NTM2NCwiZXhwIjoxNjg1ODY4OTY0fQ.eyJpZCI6MywidXNlcl90eXBlIjoxfQ.Y3VxtcJf6o4mw0boBZbvag0mEXuhIq5PktUiJgc0I6jsP9gG02nhislPamJ-WiUE0uMsfQVQFo-5X8nk8aq98Q', '2023-06-04 16:56:04', 1, 0, '2022-10-19 17:30:22', '2023-06-04 15:56:04');
INSERT INTO `user_token` VALUES (9, 2023010811531460, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTUwNzUzMywiZXhwIjoxNjg1NTExMTMzfQ.eyJpZCI6MjAyMzAxMDgxMTUzMTQ2MCwidXNlcl90eXBlIjowfQ.kKqPFNsiPWavR9qZgURFOJdG2ZG0pnTMv0b8uBbSaJnuhQnfGt0u3RYxq_E9IgkVZ9a6Qvk355wv3VPrTYPpPw', '2023-05-31 13:32:13', 1, 0, '2023-01-08 11:54:31', '2023-05-31 12:32:13');
INSERT INTO `user_token` VALUES (10, 2022101916565937, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4OTE2MDAzMiwiZXhwIjoxNjg5NTIwMDMyfQ.eyJpZCI6MjAyMjEwMTkxNjU2NTkzNywidXNlcl90eXBlIjowfQ.hlX6ake8wWgn30RYBDNrUceBe2VoLn_S17uJ49B6ujapNTx-7NJpNddMDPNbVSHBRzPbmoMkC3JAyVotiUz4mw', '2023-07-16 23:07:12', 1, 0, '2023-01-11 09:31:55', '2023-07-12 19:07:12');
INSERT INTO `user_token` VALUES (11, 2023021919383065, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTE4Nzc5MywiZXhwIjoxNjg1MTkxMzkzfQ.eyJpZCI6MjAyMzAyMTkxOTM4MzA2NSwidXNlcl90eXBlIjowfQ.6n5EC8VKI6z1R3NJAW5xIq0jmZiUl8-o1_zBV8qGlEwV0xkt2BBe6i9HpdoFJkNjblBn-qPwEFa-rLW_uf-JuQ', '2023-05-27 20:43:13', 1, 0, '2023-02-19 19:38:24', '2023-05-27 19:43:13');
INSERT INTO `user_token` VALUES (12, 2023022021261429, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY3Njg5OTc0MywiZXhwIjoxNjc2OTAzMzQzfQ.eyJpZCI6MjAyMzAyMjAyMTI2MTQyOSwidXNlcl90eXBlIjowfQ.BoGOa7zGsl0Mx0CAHYS1CsCbZsaeIE_RsAb_Pe3d-2Mvt-Pj_zmDe7i-iw-YhvDXAZWUW23J3ndAqdw5dsZ2nA', '2023-02-20 22:29:03', 1, 0, '2023-02-20 21:28:15', '2023-02-20 21:29:02');
INSERT INTO `user_token` VALUES (13, 2023022511534572, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY3NzgzNDU4NSwiZXhwIjoxNjc3ODM4MTg1fQ.eyJpZCI6MjAyMzAyMjUxMTUzNDU3MiwidXNlcl90eXBlIjowfQ.qg_MM0eZHePXHV8zo2cH85VpfpYt1XUKnyC7WysExSS2YLGur_EBHioiDvfjAQ7iM9uvmfI2fQM7-HNH3mI4Ig', '2023-03-03 18:09:45', 1, 0, '2023-02-25 11:53:59', '2023-03-03 17:09:45');
INSERT INTO `user_token` VALUES (14, 2023022511551906, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY3OTAzNzU0OCwiZXhwIjoxNjc5MDQxMTQ4fQ.eyJpZCI6MjAyMzAyMjUxMTU1MTkwNiwidXNlcl90eXBlIjowfQ.opORcvoW2qsLLu0vq97EHO32nDyM_H-ZRg3JUP2kL7ZGjQWyW2f_XEgoxRxcAaFoB3wQ5qJ4PBmc_EdATFA6cg', '2023-03-17 16:19:08', 1, 0, '2023-02-25 11:57:07', '2023-03-17 15:19:08');
INSERT INTO `user_token` VALUES (15, 2023022511551910, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4MTc4ODk3MSwiZXhwIjoxNjgxNzkyNTcxfQ.eyJpZCI6MjAyMzAyMjUxMTU1MTkxMCwidXNlcl90eXBlIjowfQ.EiqIVbL8C7ssgc8HS19tFqOLbN1S0IzoEFFM_nblYR0L5T8RWVFgfClr2yvmoTPkEW-L68Ejp-AZ-eqVQbn8Tw', '2023-04-18 12:36:11', 1, 0, '2023-03-03 15:42:23', '2023-04-18 11:36:11');
INSERT INTO `user_token` VALUES (16, 2023032213102608, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY3OTQ2MTgxNywiZXhwIjoxNjc5NDY1NDE3fQ.eyJpZCI6MjAyMzAzMjIxMzEwMjYwOCwidXNlcl90eXBlIjowfQ.1-IlkGCA-sbfkslue9-HI3qzOkho76NSKTNKRmihKxAhcox7HzzVhl9YfLJD1bl3lvCfOKE3UAyz1jKBItxGtw', '2023-03-22 14:10:17', 1, 0, '2023-03-22 13:10:17', '2023-03-22 13:10:17');
INSERT INTO `user_token` VALUES (17, 2023041223478759, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4MTMxNDk5OSwiZXhwIjoxNjgxMzE4NTk5fQ.eyJpZCI6MjAyMzA0MTIyMzQ3ODc1OSwidXNlcl90eXBlIjowfQ.eQq5zhLRdUR32Hqrzv9TQkx7NAJXLW5sWuWtGWkrsr9q387UyeoC5WMHFVZ0k23JAdPjMNxTyIrLLHtVRSvxzg', '2023-04-13 00:56:39', 1, 0, '2023-04-12 23:47:18', '2023-04-12 23:56:39');
INSERT INTO `user_token` VALUES (18, 2023052319123652, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxNjUzMjk4MywiZXhwIjoxNzE2ODkyOTgzfQ.eyJpZCI6MjAyMzA1MjMxOTEyMzY1MiwidXNlcl90eXBlIjowfQ.qzCpLnmlLuy0b0xAv33YpKl2SeaT14F7dGNfZQAyb-Zv3sv5lJ9il1zm7XruWKf7DqrvtwMdGmkIW5W8kGJ0Lg', '2024-05-28 18:43:03', 1, 0, '2023-05-23 19:12:59', '2024-05-24 06:43:03');
INSERT INTO `user_token` VALUES (19, 2023053118014682, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTUyNzMxMywiZXhwIjoxNjg1NTMwOTEzfQ.eyJpZCI6MjAyMzA1MzExODAxNDY4MiwidXNlcl90eXBlIjowfQ.pa5b3DF8kIAqaiPC6MT5gj_skgdv60Q-xqiluMGYb0UU5a_ZpCiw6A-CrAlSKnhtilllv5XUqjNFzWCCqIyccw', '2023-05-31 19:01:53', 1, 0, '2023-05-31 18:01:53', '2023-05-31 18:01:53');
INSERT INTO `user_token` VALUES (20, 2023060119434180, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjI4MTA1NCwiZXhwIjoxNjg2NjQxMDU0fQ.eyJpZCI6MjAyMzA2MDExOTQzNDE4MCwidXNlcl90eXBlIjowfQ.aeFynfI6CB2cGbqY0FAqIpqiQLmKGan4VfS_vZHWe--BOSOr59zGCBGUPBkQfhCkbizuXHAHgnomzp7nQW2pcg', '2023-06-13 15:24:14', 1, 0, '2023-06-01 19:43:10', '2023-06-09 11:24:14');
INSERT INTO `user_token` VALUES (21, 2023060218152703, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTcwMDk1NCwiZXhwIjoxNjg1NzA0NTU0fQ.eyJpZCI6MjAyMzA2MDIxODE1MjcwMywidXNlcl90eXBlIjowfQ.ZFTPkE2baWlY-R1Cu0MCykyTZk8JTBoJXW1Ly-bX9dnIKEhlbyBzayCKXlTHqxzGah3CwqU5BwkwYYyHtG6raA', '2023-06-02 19:15:54', 1, 0, '2023-06-02 18:15:54', '2023-06-02 18:15:54');
INSERT INTO `user_token` VALUES (22, 2023060218164896, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTcwMTA1OSwiZXhwIjoxNjg1NzA0NjU5fQ.eyJpZCI6MjAyMzA2MDIxODE2NDg5NiwidXNlcl90eXBlIjowfQ.z8qBpACsx00skhnajNNP-QQGdevb3lgIMZpESQ7B7uIErEKrH5qNrMwYJIp8azVbOzeQT8JfsoFf8CS26r2Wqg', '2023-06-02 19:17:39', 1, 0, '2023-06-02 18:17:07', '2023-06-02 18:17:39');
INSERT INTO `user_token` VALUES (23, 2023060419198052, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTg3NzU2MCwiZXhwIjoxNjg1ODgxMTYwfQ.eyJpZCI6MjAyMzA2MDQxOTE5ODA1MiwidXNlcl90eXBlIjowfQ.auJjzwMqwhNWbqFhFvJ0klwTUSBCleQBjUZ4JzTfIJ38coZ4VDzafETXuTo84S5u-yii0aLaoRNtdiTnpuQ1hQ', '2023-06-04 20:19:20', 1, 0, '2023-06-04 19:19:20', '2023-06-04 19:19:20');
INSERT INTO `user_token` VALUES (24, 2023060516155932, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTk2NTk0NCwiZXhwIjoxNjg1OTY5NTQ0fQ.eyJpZCI6MjAyMzA2MDUxNjE1NTkzMiwidXNlcl90eXBlIjowfQ.f45-hHB_NKs75Evp7r2LThLdERjJhunGAcrZ8UG6sZU5xIx0XIPBE4vzh6YIl4F2AglPcZbyZXS4Cw4SoVLQAQ', '2023-06-05 20:52:24', 1, 0, '2023-06-05 16:15:38', '2023-06-05 19:52:24');
INSERT INTO `user_token` VALUES (25, 2023060519549435, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjI4MTA0NywiZXhwIjoxNjg2NjQxMDQ3fQ.eyJpZCI6MjAyMzA2MDUxOTU0OTQzNSwidXNlcl90eXBlIjowfQ.rpwzRN71m7VMRZuyWbQeRwbyP8RBB6Kl2co7mw750OPOvICdP3lwvlExrcAxMaj_z_VggpR3XDE1CEyR5Rzk6w', '2023-06-13 15:24:07', 1, 0, '2023-06-05 19:54:30', '2023-06-09 11:24:07');
INSERT INTO `user_token` VALUES (26, 2023060520134879, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NTk2NzE4NiwiZXhwIjoxNjg1OTcwNzg2fQ.eyJpZCI6MjAyMzA2MDUyMDEzNDg3OSwidXNlcl90eXBlIjowfQ.y6QOteahaPA0e_ItOAVnmN_jCd2CgC3wTIM3D6JcDXHGOAPDkdghmt3Bmo2JcE-QOayIjXnq9ITf_MpxTzfgXg', '2023-06-05 21:13:06', 1, 0, '2023-06-05 20:13:06', '2023-06-05 20:13:06');
INSERT INTO `user_token` VALUES (27, 2023060520153196, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEwNDAzOCwiZXhwIjoxNjg2NDY0MDM4fQ.eyJpZCI6MjAyMzA2MDUyMDE1MzE5NiwidXNlcl90eXBlIjowfQ.va9gL-0iIXdtm8EOoXMg8H8VoUV4jKyyCLwU8OLS1UE0PrxiypY7PPmBv8YGKAdMxmusxwcoTq8SQVapRfrJOQ', '2023-06-11 14:13:58', 1, 0, '2023-06-05 20:15:43', '2023-06-07 10:13:58');
INSERT INTO `user_token` VALUES (28, 2023060609517693, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjQ3MTM1MSwiZXhwIjoxNjg2ODMxMzUxfQ.eyJpZCI6MjAyMzA2MDYwOTUxNzY5MywidXNlcl90eXBlIjowfQ.CX2WyjQb9bpQWglktt19NTJWoPQHzXce_w5Ew66rD2aKDutIsCqJG7MaG7_Q4yldazyV6SMygPGhYs4g-Zj7aw', '2023-06-15 20:15:51', 1, 0, '2023-06-06 09:51:06', '2023-06-11 16:15:51');
INSERT INTO `user_token` VALUES (29, 2023060618151640, 1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4ODk3MDY4OCwiZXhwIjoxNjg5MzMwNjg4fQ.eyJpZCI6MjAyMzA2MDYxODE1MTY0MCwidXNlcl90eXBlIjoxfQ.OVGxtJQBhXfqXDM45_VVqe15gobV2NU0Sero0nluabt7NqW6TuJ6_rEIXBsZIYLn0DaSx-aXcY16BxnoixwWEQ', '2023-07-14 18:31:28', 1, 0, '2023-06-06 18:16:41', '2023-07-10 14:31:28');
INSERT INTO `user_token` VALUES (30, 2023060618188036, 1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjIyNzAyNywiZXhwIjoxNjg2NTg3MDI3fQ.eyJpZCI6MjAyMzA2MDYxODE4ODAzNiwidXNlcl90eXBlIjoxfQ.7lLQbaMryr4oIxV2g3jjQ9V2z4gPXAjxeH75WznSIws2u-i49WwOY4uEUH_tYkZmycK0lhyarcySTPdW2ZrsnQ', '2023-06-13 00:23:47', 1, 0, '2023-06-06 18:37:52', '2023-06-08 20:23:47');
INSERT INTO `user_token` VALUES (31, 2023060710227948, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjMwNzEyNywiZXhwIjoxNjg2NjY3MTI3fQ.eyJpZCI6MjAyMzA2MDcxMDIyNzk0OCwidXNlcl90eXBlIjowfQ.78bK4CXwNW8zMpzDQKx-BTzAQBd4Xf5eEzDEx6Oe2wvvhgDNoRxMJA45W7LKcTJN1rT5emWXdKwg8C3uZSYJ_w', '2023-06-13 22:38:47', 1, 0, '2023-06-07 10:22:28', '2023-06-09 18:38:47');
INSERT INTO `user_token` VALUES (32, 2, 1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxNzQ4NTY3NCwiZXhwIjoxNzE3ODQ1Njc0fQ.eyJpZCI6MiwidXNlcl90eXBlIjoyfQ.HVI4N3YD9NQWgMSfQvKpYz-1WOEKlJORVFm-Xh63oRiXJJMY2o9xqILd1aJ0nxfyr9mfdUVa2IiH_jm8D3sBTA', '2024-06-08 19:21:14', 1, 0, '2023-06-07 10:59:16', '2024-06-04 07:21:14');
INSERT INTO `user_token` VALUES (33, 2023051109588542, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjI4MjQ3OSwiZXhwIjoxNjg2Mjg2MDc5fQ.eyJpZCI6MjAyMzA1MTEwOTU4ODU0MiwidXNlcl90eXBlIjowfQ.MYn6aHyOuCbkzdEBYYmo-jUS956XaX0QYoHobdE4UrvmGJaRwhXQvfoYlFuEd9ZXnjhFBp_cmfOmGsq_R3tznQ', '2023-06-09 12:47:59', 1, 0, '2023-06-07 19:17:42', '2023-06-09 11:47:59');
INSERT INTO `user_token` VALUES (34, 2023060719410532, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEzODExMCwiZXhwIjoxNjg2NDk4MTEwfQ.eyJpZCI6MjAyMzA2MDcxOTQxMDUzMiwidXNlcl90eXBlIjowfQ.nC6_YgkYLu87wpHNm1oKPmSixB80CHdz63m57Jn5x5-J-Xbnw7aWfWlrHu53OOPApLTNqMryXYWHf9m_xB7Ikw', '2023-06-11 23:41:50', 1, 0, '2023-06-07 19:41:50', '2023-06-07 19:41:50');
INSERT INTO `user_token` VALUES (35, 2023060719426850, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEzODEzMiwiZXhwIjoxNjg2NDk4MTMyfQ.eyJpZCI6MjAyMzA2MDcxOTQyNjg1MCwidXNlcl90eXBlIjowfQ.hmkDBwbv0N7raE624BsCRyq3WtMW8HLxkEXPruW5Dh426jWAXCxb0eHFm4NNJtGRcE9hnarwb7jgirZB4V0xiQ', '2023-06-11 23:42:12', 1, 0, '2023-06-07 19:42:12', '2023-06-07 19:42:12');
INSERT INTO `user_token` VALUES (36, 2023060720019738, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEzOTI5NywiZXhwIjoxNjg2NDk5Mjk3fQ.eyJpZCI6MjAyMzA2MDcyMDAxOTczOCwidXNlcl90eXBlIjowfQ.uhQyHqgOJyQCyUZDcHI1_dK54cTbG8XwAAFSLa7snJWjyXhboKGRevsjqvHzVcZjusIpOo1RnyPHGrVeqhOL9w', '2023-06-12 00:01:37', 1, 0, '2023-06-07 20:01:37', '2023-06-07 20:01:37');
INSERT INTO `user_token` VALUES (37, 2023060720015430, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEzOTMxNiwiZXhwIjoxNjg2NDk5MzE2fQ.eyJpZCI6MjAyMzA2MDcyMDAxNTQzMCwidXNlcl90eXBlIjowfQ.-26clmljlLJW_MHxq39N96iARxoTzV1ROfWEEnHAz1naRuynb0lpuwh-KsKDYIo0Gshgk8LZAuijXXg8NuRbZw', '2023-06-12 00:01:56', 1, 0, '2023-06-07 20:01:56', '2023-06-07 20:01:56');
INSERT INTO `user_token` VALUES (38, 2023060720025130, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEzOTMyOSwiZXhwIjoxNjg2NDk5MzI5fQ.eyJpZCI6MjAyMzA2MDcyMDAyNTEzMCwidXNlcl90eXBlIjowfQ.1aLzVm_JwsIlLXfM91oimVrk1SEQkCPETAm8NPt1pa498Q-ndIgCHGmcWrG6pABrm08MrFl4TBdabMxHryV7Hg', '2023-06-12 00:02:09', 1, 0, '2023-06-07 20:02:09', '2023-06-07 20:02:09');
INSERT INTO `user_token` VALUES (39, 2023060720026517, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEzOTM0NSwiZXhwIjoxNjg2NDk5MzQ1fQ.eyJpZCI6MjAyMzA2MDcyMDAyNjUxNywidXNlcl90eXBlIjowfQ.-6FkNy_XxcTY7Tz9gaj6bPg7VQ6FALE1lZDIXDTWsUOiAYu4f8y09z9Tla3IaV3gex8umE6B_UG_kZ3OgfTtpQ', '2023-06-12 00:02:25', 1, 0, '2023-06-07 20:02:25', '2023-06-07 20:02:25');
INSERT INTO `user_token` VALUES (40, 2023060720021463, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjEzOTM2MSwiZXhwIjoxNjg2NDk5MzYxfQ.eyJpZCI6MjAyMzA2MDcyMDAyMTQ2MywidXNlcl90eXBlIjowfQ.jxLdNxKVTw8C9Ffd9p6OA1PgZL6PQ3ZueJrWQHrDvn71xkO-gcvGlX9RCbmLSlwhInhDgrXQ0eTb8DBiE8SEUA', '2023-06-12 00:02:41', 1, 0, '2023-06-07 20:02:41', '2023-06-07 20:02:41');
INSERT INTO `user_token` VALUES (41, 2023060717517293, 1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjM4MzQ4NSwiZXhwIjoxNjg2NzQzNDg1fQ.eyJpZCI6MjAyMzA2MDcxNzUxNzI5MywidXNlcl90eXBlIjoxfQ.b925G9hxkZYDCY7jNbDCjsuMLmS4HV5xoqINixt4yzFrp6-iEK6dySZxj_fG_a-WuUP7LqoNrH4xU9VueNPLLg', '2023-06-14 19:51:25', 1, 0, '2023-06-07 20:42:31', '2023-06-10 15:51:25');
INSERT INTO `user_token` VALUES (42, 2023060810242379, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjMwODg1OCwiZXhwIjoxNjg2NjY4ODU4fQ.eyJpZCI6MjAyMzA2MDgxMDI0MjM3OSwidXNlcl90eXBlIjowfQ.es0su9vWJ0ooUFnmEOT6fNA-fW_AafJRDtuYSRMwxnk6fPSM2LhDg8TrLl3eeZ3W19zTBoe6I6qoQUlmH_hZ2A', '2023-06-13 23:07:38', 1, 0, '2023-06-08 10:24:59', '2023-06-09 19:07:38');
INSERT INTO `user_token` VALUES (43, 2023060810450698, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjMyNCwiZXhwIjoxNjg2NTUyMzI0fQ.eyJpZCI6MjAyMzA2MDgxMDQ1MDY5OCwidXNlcl90eXBlIjowfQ.PadHl590rriqXXCRsL5siz0-W32BcQ4Gy8oijcl03JkF-jfzKRU155xuUcdXnUe3rDR1lEjv9ijWpRHUSYqWQg', '2023-06-12 14:45:24', 1, 0, '2023-06-08 10:45:24', '2023-06-08 10:45:24');
INSERT INTO `user_token` VALUES (44, 2023060810452314, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjM0NCwiZXhwIjoxNjg2NTUyMzQ0fQ.eyJpZCI6MjAyMzA2MDgxMDQ1MjMxNCwidXNlcl90eXBlIjowfQ.GLWXMtJ0Tkw-7kGEmEPay-kv-KVdlNvb5vP25q82aO--GL2RARRD8_W2fGpQ94EOhHr6133z-4pERRmsnmV9FA', '2023-06-12 14:45:44', 1, 0, '2023-06-08 10:45:44', '2023-06-08 10:45:44');
INSERT INTO `user_token` VALUES (45, 2023060810457302, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxMTQ1MzIyNywiZXhwIjoxNzExODEzMjI3fQ.eyJpZCI6MjAyMzA2MDgxMDQ1NzMwMiwidXNlcl90eXBlIjowfQ.1vVVVVhPUkaTsiQq79K3f_dFUOQCoA6cht-tIAmV4CxmyeTI32_i-vj770sioj-nr2jn_cKJDmJ7-bhL4Ig2kw', '2024-03-30 23:40:27', 1, 0, '2023-06-08 10:45:57', '2024-03-26 11:40:27');
INSERT INTO `user_token` VALUES (46, 2023060810467063, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjM3MSwiZXhwIjoxNjg2NTUyMzcxfQ.eyJpZCI6MjAyMzA2MDgxMDQ2NzA2MywidXNlcl90eXBlIjowfQ.XONTiCNSG4K1-7qWQwMeI0e4vWQCLCTovnKchIPsWrJ83VEPOn3TF2vK622jk3yMsFBwoAm25zIX-VfdJsyrpw', '2023-06-12 14:46:11', 1, 0, '2023-06-08 10:46:11', '2023-06-08 10:46:11');
INSERT INTO `user_token` VALUES (47, 2023060810464716, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjM4NSwiZXhwIjoxNjg2NTUyMzg1fQ.eyJpZCI6MjAyMzA2MDgxMDQ2NDcxNiwidXNlcl90eXBlIjowfQ.gHIlLSnTE0VJAXWQZoKOb2ayu-XWSJjdYTJiWlsENZqXkLKDBdhbp9XlHd1zQ3S5u3A7o7rvWI_UWxsV80uvcQ', '2023-06-12 14:46:25', 1, 0, '2023-06-08 10:46:25', '2023-06-08 10:46:25');
INSERT INTO `user_token` VALUES (48, 2023060810468619, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjQwMywiZXhwIjoxNjg2NTUyNDAzfQ.eyJpZCI6MjAyMzA2MDgxMDQ2ODYxOSwidXNlcl90eXBlIjowfQ.iMznY8tKCezc0dsB8hPtsyQiS9pGKdDcGHTjDOK6xBvEsE4HfC-MZVzxasLKSfvt2ZrNr-FJUO9ye8FCkWLkMA', '2023-06-12 14:46:43', 1, 0, '2023-06-08 10:46:43', '2023-06-08 10:46:43');
INSERT INTO `user_token` VALUES (49, 2023060810461802, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjQxNywiZXhwIjoxNjg2NTUyNDE3fQ.eyJpZCI6MjAyMzA2MDgxMDQ2MTgwMiwidXNlcl90eXBlIjowfQ.Skh4d5OxJmLCuXVdEQkisYavanE4W60Y8HaMFtuofNGlpTDVxEm5uom6ytsnugOrd-qrCKGljAKz64_RTfptdQ', '2023-06-12 14:46:57', 1, 0, '2023-06-08 10:46:57', '2023-06-08 10:46:57');
INSERT INTO `user_token` VALUES (50, 2023060810471602, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjQzMSwiZXhwIjoxNjg2NTUyNDMxfQ.eyJpZCI6MjAyMzA2MDgxMDQ3MTYwMiwidXNlcl90eXBlIjowfQ.V3fjUZnayWfRn-M6H0c89ocbFoPCkF613GgwnQvDK4MFH8gu6frWHbeID13Q-brpiKWwEqw36KDSnu8eJkXrDg', '2023-06-12 14:47:11', 1, 0, '2023-06-08 10:47:11', '2023-06-08 10:47:11');
INSERT INTO `user_token` VALUES (51, 2023060810473960, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjQ0NCwiZXhwIjoxNjg2NTUyNDQ0fQ.eyJpZCI6MjAyMzA2MDgxMDQ3Mzk2MCwidXNlcl90eXBlIjowfQ.oebpPXj8w_j4PVCGHfsCk2inG8lmJAtKAoBUvJ2ArnNs0gD3ex0eiWIIxwvfGVcWgt1aaH663Cw1f5MjlGoO7Q', '2023-06-12 14:47:24', 1, 0, '2023-06-08 10:47:24', '2023-06-08 10:47:24');
INSERT INTO `user_token` VALUES (52, 2023060810485718, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjQ5MSwiZXhwIjoxNjg2NTUyNDkxfQ.eyJpZCI6MjAyMzA2MDgxMDQ4NTcxOCwidXNlcl90eXBlIjowfQ.WoWMJ_Tho7UMwH35hqVuTimv2yKcQFGnBY1BOlV2wiOReC-iT9BdvK-AYHSA_5XUVbHQI06j-hUiKrNPImu4UA', '2023-06-12 14:48:11', 1, 0, '2023-06-08 10:48:11', '2023-06-08 10:48:11');
INSERT INTO `user_token` VALUES (53, 2023060810480719, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjUwNSwiZXhwIjoxNjg2NTUyNTA1fQ.eyJpZCI6MjAyMzA2MDgxMDQ4MDcxOSwidXNlcl90eXBlIjowfQ.yux-D-iYV7SXVFWD8Pn97isAXIMkiAuh8rmXwdyP5VfCrxH7SFCUxCJvWgofIlXvnXsXrKQG5Q2rN9pQIrvWOQ', '2023-06-12 14:48:25', 1, 0, '2023-06-08 10:48:25', '2023-06-08 10:48:25');
INSERT INTO `user_token` VALUES (54, 2023060810485408, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjUyNiwiZXhwIjoxNjg2NTUyNTI2fQ.eyJpZCI6MjAyMzA2MDgxMDQ4NTQwOCwidXNlcl90eXBlIjowfQ.eVGarTohx9nM9gartqBvkvsXNN_t-Go2jrNBXI7K0QzGJcvxt1ufbVYcXZ2dMurOCAjMXcWjxhdaYuXPPNw1Mw', '2023-06-12 14:48:46', 1, 0, '2023-06-08 10:48:46', '2023-06-08 10:48:46');
INSERT INTO `user_token` VALUES (55, 2023060810481865, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjUzOSwiZXhwIjoxNjg2NTUyNTM5fQ.eyJpZCI6MjAyMzA2MDgxMDQ4MTg2NSwidXNlcl90eXBlIjowfQ.AQOP2eM8bXafsAJDLZ-WxXSgqgoaQ0E1Cu2_iPm2aYiozciwyXr5Ot2uPkvpALVzbt4g_cDyE55veTErt4nukQ', '2023-06-12 14:48:59', 1, 0, '2023-06-08 10:48:59', '2023-06-08 10:48:59');
INSERT INTO `user_token` VALUES (56, 2023060810490134, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMTMzMjc3MSwiZXhwIjoxNzAxNjkyNzcxfQ.eyJpZCI6MjAyMzA2MDgxMDQ5MDEzNCwidXNlcl90eXBlIjowfQ.wTZu1HL7KKG-dEIREBtyTc72f0wGTdAkDwdFfsRf_TxBCtcL3jpuEOKvLFj8zbyIhWHg-qJpA8_zjQMgDhF4eg', '2023-12-04 20:26:11', 1, 0, '2023-06-08 10:49:17', '2023-11-30 08:26:11');
INSERT INTO `user_token` VALUES (57, 2023060810494863, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjU3MSwiZXhwIjoxNjg2NTUyNTcxfQ.eyJpZCI6MjAyMzA2MDgxMDQ5NDg2MywidXNlcl90eXBlIjowfQ.ddD4tWA8knmdzMNn2b5xAxEJe3Sdw1tvzmKqIvj0I-SMyqvw66bEdj81wsqJGa94B-v6dkNkFy-MPV1Cfk-Fhg', '2023-06-12 14:49:31', 1, 0, '2023-06-08 10:49:31', '2023-06-08 10:49:31');
INSERT INTO `user_token` VALUES (58, 2023060810493970, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjU4NiwiZXhwIjoxNjg2NTUyNTg2fQ.eyJpZCI6MjAyMzA2MDgxMDQ5Mzk3MCwidXNlcl90eXBlIjowfQ.2RUqtUK3SktIup90R_QOSDK4WhAF2yfrxH5EZ2kqYunWEE1zfjRSELOuQmUzxXD2dG7InJelc6YSJzrSECxzWQ', '2023-06-12 14:49:46', 1, 0, '2023-06-08 10:49:46', '2023-06-08 10:49:46');
INSERT INTO `user_token` VALUES (59, 2023060810493901, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjYwMSwiZXhwIjoxNjg2NTUyNjAxfQ.eyJpZCI6MjAyMzA2MDgxMDQ5MzkwMSwidXNlcl90eXBlIjowfQ.nQq0PCvemvACKMNePQS0gq9z1Cm_dfugKWUYhYT1bbZL7C0b2-peXxEcNPlSoGxO4Ku9TWcjO2bMR3e9nlf8jQ', '2023-06-12 14:50:01', 1, 0, '2023-06-08 10:50:01', '2023-06-08 10:50:01');
INSERT INTO `user_token` VALUES (60, 2023060810504632, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjE5MjYxNCwiZXhwIjoxNjg2NTUyNjE0fQ.eyJpZCI6MjAyMzA2MDgxMDUwNDYzMiwidXNlcl90eXBlIjowfQ.hutVjQJftIGzW3oGAnDFocDk1_rHpf3w_znF65hIa4YMw_YdGiWUXMYRi4Uep7P8Wfovs2Y8ttLZ6JCcBEMWIg', '2023-06-12 14:50:14', 1, 0, '2023-06-08 10:50:14', '2023-06-08 10:50:14');
INSERT INTO `user_token` VALUES (61, 2023060810502704, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjQ3MjA2NCwiZXhwIjoxNjg2ODMyMDY0fQ.eyJpZCI6MjAyMzA2MDgxMDUwMjcwNCwidXNlcl90eXBlIjowfQ.E9N44xbAlsnIHViHnq18JTsdk1hm6TxDKyYxxX2lqclkXJiG3Nc0gAoP8vHD0zXxScQaBkxI_3cpAF7dBoZRjQ', '2023-06-15 20:27:44', 1, 0, '2023-06-08 10:50:27', '2023-06-11 16:27:44');
INSERT INTO `user_token` VALUES (62, 2023060911428390, 1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NjQ2MzcwNSwiZXhwIjoxNjg2ODIzNzA1fQ.eyJpZCI6MjAyMzA2MDkxMTQyODM5MCwidXNlcl90eXBlIjoxfQ.5ubGOm4XUb6PRQT52iZRlfRMChG4XjmgpvTVhev1NJowUxzhAa4bYoCI2T_Rw_OySGMtc75W2uwKBKAI-siIww', '2023-06-15 18:08:25', 1, 0, '2023-06-09 11:42:35', '2023-06-11 14:08:25');
INSERT INTO `user_token` VALUES (63, 2023071014274137, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxMzI1Mzk2NSwiZXhwIjoxNzEzNjEzOTY1fQ.eyJpZCI6MjAyMzA3MTAxNDI3NDEzNywidXNlcl90eXBlIjowfQ.inCqrF9MDOLEY18XTwa0pTqKbhZZIvi86CT2LWVno49U7G6R-1lcRADefmgH1tWUuT4YuEV0vvFkhVmYA2tQ2w', '2024-04-20 19:52:45', 1, 0, '2023-07-10 14:27:41', '2024-04-16 07:52:45');
INSERT INTO `user_token` VALUES (64, 2023083118102805, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5MzQ3NjYzMywiZXhwIjoxNjkzODM2NjMzfQ.eyJpZCI6MjAyMzA4MzExODEwMjgwNSwidXNlcl90eXBlIjowfQ.nTRbBYdlWiVAQBdyB0B66crgTQbqKhSSqwPq2E6BciiXtQSSHa6jRfcsjQQsPAjgYOntkRcQbY55Mhymq-ep0A', '2023-09-04 22:10:33', 1, 0, '2023-08-31 18:10:33', '2023-08-31 18:10:33');
INSERT INTO `user_token` VALUES (65, 2023102116148693, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxOTQ2NjA0MCwiZXhwIjoxNzE5ODI2MDQwfQ.eyJpZCI6MjAyMzEwMjExNjE0ODY5MywidXNlcl90eXBlIjowfQ.Juvc_sD5V-flmcXfIu6wG33fWLMNb2h-03caKWoMKcR5B_bemsQXJbQvoXs5fHUNfEBowN1QNDOiEwoVf2Y8Ew', '2024-07-01 17:27:20', 1, 0, '2023-10-21 16:15:43', '2024-06-27 05:27:20');
INSERT INTO `user_token` VALUES (66, 2023110217261082, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5OTI0NjMzMCwiZXhwIjoxNjk5NjA2MzMwfQ.eyJpZCI6MjAyMzExMDIxNzI2MTA4MiwidXNlcl90eXBlIjowfQ.0BIrjosIB8CpLydOeEuuldrNtOpPnXhwHBGS7qXoebh6puAGD_9Sk5IekB9YGqGylmvKLSXV2PJdj-ly72UpxA', '2023-11-10 16:52:10', 1, 0, '2023-11-02 09:26:32', '2023-11-06 04:52:10');
INSERT INTO `user_token` VALUES (67, 2023110515244957, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxODg4NzI3NSwiZXhwIjoxNzE5MjQ3Mjc1fQ.eyJpZCI6MjAyMzExMDUxNTI0NDk1NywidXNlcl90eXBlIjowfQ.cshpiEvd2fhBdlI4fjASe4UOrToZF_XOdQRc7lUF2qI8YxxY-2kf-uPehN9Le0minwbNaAT1KrtCD0Y5Lf8lmA', '2024-06-25 00:41:15', 1, 0, '2023-11-05 07:24:25', '2024-06-20 12:41:15');
INSERT INTO `user_token` VALUES (68, 2023110612504283, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5OTI0NjM4MSwiZXhwIjoxNjk5NjA2MzgxfQ.eyJpZCI6MjAyMzExMDYxMjUwNDI4MywidXNlcl90eXBlIjowfQ.9zAbVzhLnJozrylYHNhXqMnXCnH8CfFxH-7CtszhYm61IXWIOlGLzbtNqMst_wlxmfYxRzX5WGx7oNI9RtAvnQ', '2023-11-10 16:53:01', 1, 0, '2023-11-06 04:50:26', '2023-11-06 04:53:01');
INSERT INTO `user_token` VALUES (69, 2023122119127419, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcwMzE1NzE2NywiZXhwIjoxNzAzNTE3MTY3fQ.eyJpZCI6MjAyMzEyMjExOTEyNzQxOSwidXNlcl90eXBlIjowfQ.JhHjcSi58W06yh2a_JU68USEPfjGTHwgmR5ByDy2JSwCvP9EMPDAUD0aamTgigJj6Sizag0tWtiH6M8lo0vByg', '2023-12-25 23:12:47', 1, 0, '2023-12-21 11:12:47', '2023-12-21 11:12:47');
INSERT INTO `user_token` VALUES (70, 2024053119200653, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxNzE1NDY5MywiZXhwIjoxNzE3NTE0NjkzfQ.eyJpZCI6MjAyNDA1MzExOTIwMDY1MywidXNlcl90eXBlIjowfQ.v5qQ_eVn-QLOJZhdReDUZPQbPBpcY0FvP2WlhIOjXhSYBtwxwPRtoWSVSdDz-478PJrYrhqrZkJHcG70LUFmlQ', '2024-06-04 23:24:53', 1, 0, '2024-05-31 11:20:17', '2024-05-31 11:24:53');
INSERT INTO `user_token` VALUES (71, 2024062517200487, 0, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxOTMwNzIxOCwiZXhwIjoxNzE5NjY3MjE4fQ.eyJpZCI6MjAyNDA2MjUxNzIwMDQ4NywidXNlcl90eXBlIjowfQ.8Z6-_ELjmN7A8cZFfIwqk58EsqmbRzbEqf34imk-Sd6HProkNy2GwA2Qv3RQULNxGvF8R_BgVWVJqtbCUThFUQ', '2024-06-29 21:20:18', 1, 0, '2024-06-25 09:20:18', '2024-06-25 09:20:18');

-- ----------------------------
-- View structure for v_studentscore
-- ----------------------------
DROP VIEW IF EXISTS `v_studentscore`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_studentscore` AS select `studentselectedcourse`.`studentID` AS `studentID`,`studentselectedcourse`.`courseID` AS `courseID`,`course`.`courseName` AS `courseName`,`student`.`name` AS `name`,`sys_classinfo`.`className` AS `className`,`course`.`credit` AS `credit`,`studentselectedcourse`.`score` AS `score`,`studentselectedcourse`.`addTime` AS `addTime` from (((`studentselectedcourse` join `student` on((`studentselectedcourse`.`studentID` = `student`.`studentID`))) join `sys_classinfo` on((`student`.`classID` = `sys_classinfo`.`classID`))) join `course` on((`studentselectedcourse`.`courseID` = `course`.`courseID`)));

SET FOREIGN_KEY_CHECKS = 1;
