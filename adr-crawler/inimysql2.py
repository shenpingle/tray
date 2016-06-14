#-*- coding:utf-8 -*-
###########################################################################################
#  author: luu
#  info:删除原有数据库业务信息，作重新下载、测试之用
#  Revision: 1.0
"""
    功能说明：  删除原有数据库业务信息，作重新下载、测试之用

"""
###########################################################################################

import mysql.connector

def ini():
    config = {
        'host': '192.168.1.104',
        'user': 'root',
        'password': 'root',
        'database': 'test0904'
    }

    cnn = mysql.connector.connect(**config)
    cursor = cnn.cursor()
    """
    sql_one = "drop table student"
    cursor = cnn.cursor()
    cursor.execute(sql_one)
    cnn.commit()
    """
    sql_d1 = "drop table mdr_business_gather"
    sql_d2 = "drop table mdr_adrbusiness"
    sql_d3 = "drop table mdr_faultbusiness"
    sql_d4 = "drop table mdr_icdbusiness"
    sql_d5 = "drop table mdr_devicebusiness"
    sql_d6 = "drop table mdr_errorlist"
    sql_d7 = "drop table mdr_reports"

    cursor.execute(sql_d1)
    cursor.execute(sql_d2)
    cursor.execute(sql_d3)
    cursor.execute(sql_d4)
    cursor.execute(sql_d5)
    cursor.execute(sql_d6)
    cursor.execute(sql_d7)
    cnn.commit()

    sql_one = """
        CREATE TABLE `mdr_business_gather` (
        `rec_id` bigint(20) NOT NULL auto_increment,
        `BianMa` varchar(60) NOT NULL default '' COMMENT '报表编码',
        `ProvinceName` varchar(100) default '',
        `District` varchar(100) default '',
        `County` varchar(100) default '',
        `ReportUnitName` varchar(100) default '' COMMENT '上报单位名称',
        `ReportUnitDes` varchar(100) default NULL COMMENT '上报单位描述',
        `ReportUnitAddress` varchar(100) default '' COMMENT '上报单位联系地址',
        `ReportUnitTel` varchar(100) default '' COMMENT '上报单位联系电话',
        `Postalcode` varchar(15) default '' COMMENT '邮编',
        `UnitType` varchar(20) default '' COMMENT '上报单位来源',
        `ExampleSource` varchar(10) default '' COMMENT '个例来源',
        `HappenDate` date default '0000-00-00' COMMENT '不良反应/事件发生时间',
        `KnowDate` date default '0000-00-00' COMMENT '发现或知悉时间',
        `ReportDate` date default '0000-00-00' COMMENT '报告时间',
        `AcceptDate` date default '0000-00-00' COMMENT '接受时间',
        `ProvinceReportDate` date default '0000-00-00' COMMENT '省中心接受时间',
        `StateReportDate` date default '0000-00-00' COMMENT '国家中心接受时间',
        `TrackDate` date default '0000-00-00' COMMENT '跟踪时间',
        `State` varchar(100) default NULL COMMENT '报表状态集合：已通知使用单位，已通知生产企业，已通知经营企业，已通知药监部门，未知',
        `IsADRMatch` varchar(1) default NULL COMMENT '是否是标准ADR:是,否,未(未知)',
        `ADRList` varchar(600) default NULL COMMENT 'ADR集合',
        `IsFaultMatch` varchar(1) default NULL COMMENT '是否是标准器械故障:是,否',
        `FaultList` varchar(600) default NULL COMMENT '故障集合',
        `IsDeviceMatch` varchar(1) default NULL COMMENT '是否是标准器械:是,否',
        `DeviceList` varchar(600) default NULL COMMENT '器械集合',
        `IsICDMatch` varchar(1) default NULL COMMENT '是否是标准器械预期作用:是,否',
        `ICDList` varchar(600) default NULL COMMENT '预期作用集合',
        `SuffererName` varchar(100) default '' COMMENT '患者姓名',
        `Sex` varchar(2) default '' COMMENT '性别',
        `Birthday` date default '0000-00-00' COMMENT '出生年月',
        `Age` varchar(8) default '0' COMMENT '年龄',
        `SuffererType` varchar(10) default '' COMMENT '患者分类（需要数据挖掘）婴儿、幼儿、儿童、少年、青年、中年、老年',
        `ContactTele` varchar(200) default '' COMMENT '联系方式',
        `TelePhone` varchar(200) default '' COMMENT '联系电话',
        `HospitalName` varchar(100) default '' COMMENT '医院名称',
        `DepictDispose` text COMMENT '不良反应/事件过程陈述',
        `Events` text COMMENT '事件后果:死亡,危及生命,机体功能结构永久性损伤,可能导致机体功能结构永久性损伤,需要内、外科治疗避免上述永久损伤,其它',
        `DeathDate` date default '0000-00-00' COMMENT '死亡时间',
        `IsReportAppraise` varchar(1) default NULL COMMENT '是否被报告人评价过 是 没有就不填',
        `IsReportUnitAppraise` varchar(1) default NULL COMMENT '是否被上报单位评价过',
        `IsBasicAppraise` varchar(1) default NULL COMMENT '是否被县评价过',
        `IsMunicipalAppraise` varchar(1) default NULL COMMENT '市评价过',
        `IsProvinceAppraise` varchar(1) default NULL COMMENT '是否被省评价过',
        `IsStateAppraise` varchar(1) default NULL COMMENT '是否被国家评价过',
        `IsnotifyUnit` varchar(10) default NULL COMMENT '已通知使用单位',
        `IsnotifyFactory` varchar(10) default NULL COMMENT '已通知生产企业',
        `IsnotifyShop` varchar(10) default NULL COMMENT '已通知经营企业',
        `IsnotifyGov` varchar(10) default NULL COMMENT '已通知药监部门',
        `ReportInfo` varchar(16) default '' COMMENT '报告状态:0,无；1，有评价；2，已退回',
        `IsADRorAccident` varchar(2) default '' COMMENT '是否存在故障或者adr信息:1,adr;2,故障;3故障和adr4,未知',
        `DumplicateData` varchar(20) default '' COMMENT '重复数据',
        `Reserve4` varchar(100) default NULL,
        `Reserve5` varchar(100) default NULL,
        PRIMARY KEY  (`rec_id`,`BianMa`),
        UNIQUE KEY `bianma_UnIndex` (`BianMa`),
        KEY `reportUnit_key` (`ReportUnitName`),
        KEY `happenDate_key` (`HappenDate`),
        KEY `knowDate_key` (`KnowDate`),
        KEY `reportDate_key` (`ReportDate`),
        KEY `stateReportDate_key` (`StateReportDate`)
        ) ENGINE=InnoDB AUTO_INCREMENT=116424 DEFAULT CHARSET=utf8 COMMENT='MDR系统业务主表';
    """

    sql_two = """
        CREATE TABLE `mdr_adrbusiness` (
        `rec_id` bigint(20) NOT NULL auto_increment,
        `Device_ID` varchar(20) NOT NULL default '' COMMENT '器械表编码',
        `BianMa` varchar(60) NOT NULL default '' COMMENT '报表编码',
        `ReportType` varchar(50) NOT NULL default '' COMMENT '报表类型',
        `ReportTypeDetail` varchar(100) default '' COMMENT '报表类型明细',
        `KickBackType` varchar(10) NOT NULL default '' COMMENT '报表结果',
        `FirstTraced` varchar(10) NOT NULL default '' COMMENT '首次/跟踪报告',
        `ProvinceName` varchar(100) default '',
        `District` varchar(100) default '',
        `County` varchar(100) default '',
        `FungibleReportUnit` varchar(100) default '' COMMENT '代报单位名称',
        `ReportUnitName` varchar(100) default '' COMMENT '上报单位名称',
        `ReportUnitDes` varchar(100) default NULL COMMENT '上报单位描述',
        `ReportUnitAddress` varchar(100) default '' COMMENT '上报单位联系地址',
        `ReportUnitTel` varchar(100) default '' COMMENT '上报单位联系电话',
        `Postalcode` varchar(50) default '' COMMENT '邮编',
        `UnitType` varchar(20) default '' COMMENT '报告单位类别',
        `ExampleSource` varchar(10) default '' COMMENT '个例来源',
        `HappenDate` date default '0000-00-00' COMMENT '不良反应/事件发生时间',
        `KnowDate` date default '0000-00-00' COMMENT '发现或知悉时间',
        `ReportDate` date default '0000-00-00' COMMENT '报告时间',
        `AcceptDate` date default '0000-00-00' COMMENT '接受时间',
        `ProvinceReportDate` date default '0000-00-00' COMMENT '省中心接受时间',
        `StateReportDate` date default '0000-00-00' COMMENT '国家中心接受时间',
        `TrackDate` date default '0000-00-00' COMMENT '跟踪时间',
        `State` varchar(100) default NULL,
        `IsMatchingADR` varchar(100) NOT NULL default '' COMMENT 'ADR匹配标记:是、否',
        `UnMatchADR` varchar(300) default '' COMMENT '未匹配ADR信息',
        `ADRStandardID` varchar(100) default '' COMMENT 'ADR标准编码',
        `Name` varchar(300) default '' COMMENT 'ADR标准名称',
        `SID1` varchar(100) default '' COMMENT 'ADR标准ID',
        `SubID` varchar(100) default '' COMMENT 'ADR子类标准ID',
        `SubName` varchar(300) default '' COMMENT 'ADR子类标准名称',
        `PID` varchar(100) default '' COMMENT 'ADR大类ID',
        `PName` varchar(300) default '' COMMENT 'ADR大类标准名称',
        `Reserve1` varchar(100) default NULL COMMENT '冗余',
        `Reserve2` varchar(100) default NULL COMMENT '冗余',
        `Reserve3` varchar(100) default NULL COMMENT '冗余',
        `Reserve4` varchar(100) default NULL,
        `Reserve5` varchar(100) default NULL,
        PRIMARY KEY  (`rec_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=116427 DEFAULT CHARSET=utf8 COMMENT='MDR主要伤害业务明细（1-N关系）表';
    """
    sql_three = """
        CREATE TABLE `mdr_faultbusiness` (
        `rec_id` bigint(20) NOT NULL auto_increment,
        `Device_ID` varchar(20) NOT NULL default '' COMMENT '器械表编码',
        `BianMa` varchar(60) NOT NULL default '' COMMENT '报表编码',
        `ProvinceName` varchar(100) default '' COMMENT '报单位相关行政信息',
        `District` varchar(100) default '' COMMENT '报单位相关行政信息',
        `County` varchar(100) default '' COMMENT '报单位相关行政信息',
        `ReportUnitName` varchar(100) default '' COMMENT '上报单位名称',
        `ReportUnitDes` varchar(100) default NULL COMMENT '上报单位描述',
        `ReportUnitAddress` varchar(100) default '' COMMENT '上报单位联系地址',
        `ReportUnitTel` varchar(100) default '' COMMENT '上报单位联系电话',
        `Postalcode` varchar(15) default '' COMMENT '邮编',
        `UnitType` varchar(20) default '' COMMENT '报告单位类别',
        `ExampleSource` varchar(10) default '' COMMENT '个例来源',
        `HappenDate` date default '0000-00-00' COMMENT '不良反应/事件发生时间',
        `KnowDate` date default '0000-00-00' COMMENT '发现或知悉时间',
        `ReportDate` date default '0000-00-00' COMMENT '报告时间',
        `AcceptDate` date default '0000-00-00' COMMENT '接受时间',
        `ProvinceReportDate` date default '0000-00-00' COMMENT '省中心接受时间',
        `StateReportDate` date default '0000-00-00' COMMENT '国家中心接受时间',
        `TrackDate` date default '0000-00-00' COMMENT '跟踪时间',
        `State` varchar(100) default NULL,
        `IsMatchingFault` varchar(100) NOT NULL default '' COMMENT '器械故障匹配标记:是、否',
        `UnMatchFault` varchar(300) default '' COMMENT '未匹配标准器械故障信息',
        `StandardFault` varchar(300) default '' COMMENT '器械故障标准编码',
        `SuperFaultNameID` varchar(50) default NULL COMMENT '器械故障大类标准ID',
        `SuperFaultName` varchar(300) default NULL COMMENT '器械故障大类标准名称',
        `SID` varchar(50) default '' COMMENT '器械故障标准ID',
        `Name` varchar(300) default '' COMMENT '器械故障标准名称',
        `Reserve1` varchar(100) default NULL COMMENT '冗余',
        `Reserve2` varchar(100) default NULL COMMENT '冗余',
        `Reserve3` varchar(100) default NULL COMMENT '冗余',
        `Reserve4` varchar(100) default NULL,
        `Reserve5` varchar(100) default NULL,
        PRIMARY KEY  (`rec_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=288212 DEFAULT CHARSET=utf8 COMMENT='MDR器械主要故障业务明细（1-N关系）表';
    """

    sql_four = """
        CREATE TABLE `mdr_icdbusiness` (
        `rec_id` bigint(20) NOT NULL auto_increment,
        `Device_ID` varchar(20) NOT NULL default '' COMMENT '器械表编码',
        `BianMa` varchar(60) NOT NULL default '' COMMENT '报表编码',
        `ProvinceName` varchar(100) default '',
        `District` varchar(100) default '',
        `County` varchar(100) default '',
        `ReportUnitName` varchar(100) default '' COMMENT '上报单位名称',
        `ReportUnitDes` varchar(100) default NULL COMMENT '上报单位描述',
        `ReportUnitAddress` varchar(100) default '' COMMENT '上报单位联系地址',
        `ReportUnitTel` varchar(100) default '' COMMENT '上报单位联系电话',
        `Postalcode` varchar(15) default '' COMMENT '邮编',
        `UnitType` varchar(20) default '' COMMENT '报告单位类别',
        `ExampleSource` varchar(10) default '' COMMENT '个例来源',
        `HappenDate` date default '0000-00-00' COMMENT '不良反应/事件发生时间',
        `KnowDate` date default '0000-00-00' COMMENT '发现或知悉时间',
        `ReportDate` date default '0000-00-00' COMMENT '报告时间',
        `AcceptDate` date default '0000-00-00' COMMENT '接受时间',
        `ProvinceReportDate` date default '0000-00-00' COMMENT '省中心接受时间',
        `StateReportDate` date default '0000-00-00' COMMENT '国家中心接受时间',
        `TrackDate` date default '0000-00-00' COMMENT '跟踪时间',
        `State` varchar(100) default NULL,
        `IsMatchingAffect` varchar(100) default '' COMMENT '标准器械预期作用匹配标记:是、否',
        `UnMatchAffect` varchar(300) default '' COMMENT '未匹配标准器械预期作用信息',
        `AffectStandardName` varchar(300) default '' COMMENT '标准器械预期作用名称',
        `icd_a_id` varchar(100) default '' COMMENT 'icd一类编码名称ID',
        `icd_a_name` varchar(300) default '' COMMENT 'icd一类编码名称名称',
        `icd_b_id` varchar(100) default '' COMMENT 'icd二类编码名称名称',
        `icd_b_name` varchar(300) default '' COMMENT 'icd二类编码名称名称',
        `icd_c_id` varchar(100) default '' COMMENT 'icd三类编码名称名称',
        `icd_c_name` varchar(300) default '' COMMENT 'icd三类编码名称名称',
        `PathName` varchar(500) default NULL COMMENT '全路径名称',
        `Reserve1` varchar(100) default NULL COMMENT '冗余',
        `Reserve2` varchar(100) default NULL COMMENT '冗余',
        `Reserve3` varchar(100) default NULL COMMENT '冗余',
        `Reserve4` varchar(100) default NULL,
        `Reserve5` varchar(100) default NULL,
        PRIMARY KEY  (`rec_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=116425 DEFAULT CHARSET=utf8 COMMENT='器械预期作用业务明细（1-N关系）表';
    """
    sql_five = """
        CREATE TABLE `mdr_devicebusiness` (
        `rec_id` bigint(20) NOT NULL auto_increment,
        `business_gather_ID` varchar(20) NOT NULL default '',
        `BianMa` varchar(60) NOT NULL default '' COMMENT '报表编码',
        `ProvinceName` varchar(100) default '',
        `District` varchar(100) default '',
        `County` varchar(100) default '',
        `ReportUnitName` varchar(100) default '' COMMENT '上报单位名称',
        `ReportUnitDes` varchar(100) default NULL COMMENT '上报单位描述',
        `ReportUnitAddress` varchar(100) default '' COMMENT '上报单位联系地址',
        `ReportUnitTel` varchar(100) default '' COMMENT '上报单位联系电话',
        `Postalcode` varchar(15) default '' COMMENT '邮编',
        `UnitType` varchar(20) default '' COMMENT '报告单位类别',
        `ExampleSource` varchar(10) default '' COMMENT '个例来源',
        `HappenDate` date default '0000-00-00' COMMENT '不良反应/事件发生时间',
        `KnowDate` date default '0000-00-00' COMMENT '发现或知悉时间',
        `ReportDate` date default '0000-00-00' COMMENT '报告时间',
        `AcceptDate` date default '0000-00-00' COMMENT '接受时间',
        `ProvinceReportDate` date default '0000-00-00' COMMENT '省中心接受时间',
        `StateReportDate` date default '0000-00-00' COMMENT '国家中心接受时间',
        `TrackDate` date default '0000-00-00' COMMENT '跟踪时间',
        `State` varchar(100) default NULL,
        `IsMatchingDevice` varchar(1) NOT NULL default '' COMMENT '标准器械匹配标记:是、否',
        `UnMatchDevice` varchar(300) default '' COMMENT '未匹配标准器械信息(非标准的通用名称)',
        `DeviceStandard` varchar(300) default '' COMMENT '标准器械器械名称(标准通用名称)',
        `SID` varchar(300) default NULL,
        `Name` varchar(300) default '' COMMENT '器械品名举例名称',
        `SubID` varchar(300) default NULL,
        `SubName` varchar(300) default '' COMMENT '器械名称明细名称',
        `PID` varchar(300) default NULL,
        `PName` varchar(300) default '' COMMENT '器械大类标准名称',
        `IsMatchingFactory` varchar(50) NOT NULL default '' COMMENT '厂家匹配标记:是、否',
        `UnMatchFactory` varchar(300) default '' COMMENT '厂家未匹配名称',
        `StandardFactory` varchar(300) default '' COMMENT '标准器械生产厂家名称',
        `manufacturer_address` varchar(300) default NULL COMMENT '厂家的地址',
        `manufacturer_tel` varchar(100) default NULL COMMENT '厂家的联系电话',
        `manufacturerProvinceName` varchar(100) default NULL COMMENT '生产厂家所属省直辖市',
        `manufacturerCity` varchar(100) default NULL COMMENT '厂家所属市',
        `manufacturerCounty` varchar(100) default NULL COMMENT '厂家所属县、行政区',
        `CertificateNumber` varchar(100) default '' COMMENT '器械注册号',
        `TradeName` varchar(100) default '' COMMENT '商品名称',
        `TradeDes` varchar(100) default NULL COMMENT '商品描述',
        `classification` varchar(100) default NULL COMMENT '产品分类',
        `manageclass` varchar(10) default NULL COMMENT '管理类别',
        `classcode` varchar(10) default NULL COMMENT '产品管理分类',
        `firstreason` varchar(256) default '' COMMENT '事件发生初步原因分析',
        `firstdone` varchar(256) default '' COMMENT '事件发生初步处理情况',
        `useplace` varchar(100) default NULL COMMENT '使用场所',
        `specifications` varchar(300) default '' COMMENT '规格型号',
        `Productnumber` varchar(50) default '' COMMENT '产品编号',
        `Batchnumber` varchar(50) default '' COMMENT '产品批号',
        `operator` varchar(50) default '' COMMENT '操作人员信息:专业人员、非专业人员、患者自己、其他',
        `ImplantationDate` date default '0000-00-00' COMMENT '植入日期',
        `StopDate` date default '0000-00-00' COMMENT '停用日期',
        `EffectiveDate` date default '0000-00-00' COMMENT '医疗器械的有效日期',
        `Reserve1` varchar(100) default NULL COMMENT '冗余',
        `Reserve2` varchar(100) default NULL COMMENT '冗余',
        `Reserve3` varchar(100) default NULL COMMENT '冗余',
        `Reserve4` varchar(100) default NULL,
        `Reserve5` varchar(100) default NULL,
        PRIMARY KEY  (`rec_id`),
        UNIQUE KEY `bianma_UnIndex` (`BianMa`),
        KEY `part_of_SubName` (`SubName`(255)),
        KEY `reportUnit_key` (`ReportUnitName`),
        KEY `happenDate_key` (`HappenDate`),
        KEY `knowDate_key` (`KnowDate`),
        KEY `reportDate_key` (`ReportDate`),
        KEY `stateReportDate_key` (`StateReportDate`)
        ) ENGINE=InnoDB AUTO_INCREMENT=116423 DEFAULT CHARSET=utf8 COMMENT='器械业务明细（1-1关系）表';
    """
    sql_six = """
        CREATE TABLE `mdr_errorlist` (
        `Id` bigint(20) NOT NULL auto_increment,
        `Date` date default NULL COMMENT '日期',
        `ReportID` varchar(64) NOT NULL COMMENT '报告ID',
        `TypeTag` varchar(16) default '' COMMENT 'error:E,duplicate:D',
        `ClassTag` varchar(50) default '' COMMENT '区分器械或者药品，器械：D，药品：M',
        `ObjID` varchar(100) default '' COMMENT '18位ID',
        PRIMARY KEY  (`Id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=22161 DEFAULT CHARSET=utf8 COMMENT='重复数据';
    """
    sql_seven = """
        CREATE TABLE `mdr_reports` (
        `ReportId` int(12) NOT NULL auto_increment,
        `BianMa` varchar(30) default NULL COMMENT '编码',
        `ReportUnitStatus` varchar(1) default '' COMMENT '0:个人 1:单位 2:县 3:市 4:省 5:国家 6:无法确定',
        `ReportUnitWork` varchar(50) default '' COMMENT '报告人职业:医师 、技师 、护士、工程师、其他',
        `ReportUnitMail` varchar(50) default '' COMMENT '报告人电子邮件',
        `ReportUnitnName` varchar(100) default '' COMMENT '报告单位名称',
        `ReportUnitLinkman` varchar(100) default '' COMMENT '报告单位联系人',
        `ReportUnitPhone` varchar(50) default '' COMMENT '报告单位联系电话',
        `ReportUnitAutograph` varchar(50) default '' COMMENT '报告单位人签名',
        `ReportAppraiseDate` date default '0000-00-00' COMMENT '联性评价时间',
        `ReportRequirement` varchar(10) default '' COMMENT '是否符合报告要求:是 否',
        `ReportRequirementReason` varchar(200) default '' COMMENT '不符合报告要求的原因',
        `ReportPreliminaryAnalysisOfEvents` varchar(200) default '' COMMENT '事件初步原因分析',
        `ReportUnitComments` text COMMENT '备注',
        `ReportUnitAttachments` text COMMENT '附件',
        `ReportUnitADRDateAnalyse` varchar(50) default NULL COMMENT '使用医疗器械与已发生/可能发生的伤害事件之间是否具有合理的先后时间顺序：有、无',
        `ReportUnitADRTypeAnalyse` varchar(50) default NULL COMMENT '发生/可能发生的伤害事件是否属于所使用医疗器械可能导致的伤害类型：是、否、无法确定',
        `ReportUnitOtherRelatedAnalyse` varchar(50) default NULL COMMENT '已发生/可能发生的伤害事件是否可以用合并用药和/或械的作用、患者病情或其他非医疗器械因素来解释：是、否、无法确定',
        `ReportUnitAppraise` varchar(100) default '' COMMENT '报告单位评价：很有可能，可能有关，可能无关，无法确定',
        `DateTag` date default NULL,
        PRIMARY KEY  (`ReportId`)
        ) ENGINE=InnoDB AUTO_INCREMENT=27354803 DEFAULT CHARSET=utf8 COMMENT='MDR系统报表业务表1-N';
    """

    #cursor = cnn.cursor()
    try:
        #
        cursor.execute(sql_one)
        cursor.execute(sql_two)
        cursor.execute(sql_three)
        cursor.execute(sql_four)
        cursor.execute(sql_five)
        cursor.execute(sql_six)
        cursor.execute(sql_seven)
        cnn.commit()
    except mysql.connector.Error as e:
        #
        print('create table orange fails!{}'.format(e))

    print u"New table already Created...."

if __name__ == "__main__":
    ini()