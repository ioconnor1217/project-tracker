USE [ProjectTracker]
GO

DROP TABLE IF EXISTS [dbo].[ProjectDetail]
DROP TABLE IF EXISTS [dbo].[ProjectConsultant]
DROP TABLE IF EXISTS [dbo].[Consultant]
DROP TABLE IF EXISTS [dbo].[Login]
DROP TABLE IF EXISTS [dbo].[Project]
DROP TABLE IF EXISTS [dbo].[Client]
GO

CREATE TABLE [dbo].[Client](
	[ClientID] [smallint] IDENTITY(1,1) NOT NULL,
	[Company] [varchar](255) NOT NULL,  
	[Street] [varchar](50) NOT NULL,
	[City] [varchar](50) NOT NULL,
	[State] [char](2) NOT NULL,  
	[PostalCode] [char](5) NOT NULL,
	[PhoneNumber] [varchar](15) NOT NULL,
	[EmailAddress] [varchar](50) NOT NULL,
	[CreatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [CreatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    [UpdatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [UpdatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT [XPKClient] PRIMARY KEY CLUSTERED ([ClientID] ASC),
 CONSTRAINT [XAK1Client] UNIQUE NONCLUSTERED ([Company] ASC)
 )
GO

CREATE TABLE [dbo].[Project](
	[ProjectID] [smallint] IDENTITY(1,1) NOT NULL,
	[Project] [varchar](100) NOT NULL,  
	[CreatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [CreatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    [UpdatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [UpdatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT [XPKProject] PRIMARY KEY CLUSTERED ([ProjectID] ASC),
 CONSTRAINT [XAK1Project] UNIQUE NONCLUSTERED ([Project] ASC)
 )
GO

CREATE TABLE [dbo].[Login](
	[LoginID] [smallint] IDENTITY(1,1) NOT NULL,
	[Login] [varchar](50) NOT NULL,
	[Password] [varchar](100) NOT NULL,
	[CreatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [CreatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    [UpdatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [UpdatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT [XPKLogin] PRIMARY KEY CLUSTERED ([LoginID] ASC),
 CONSTRAINT [XAK1Login] UNIQUE NONCLUSTERED ([Login]) 
)
GO

CREATE TABLE [dbo].[Consultant](
	[ConsultantID] [smallint] IDENTITY(1,1) NOT NULL,
	[LoginID] [smallint] NOT NULL,
	[FirstName] [varchar](50) NOT NULL,  
	[LastName] [varchar](50) NOT NULL,
	[City] [varchar](50) NOT NULL,
	[State] [char](2) NOT NULL,  
	[PostalCode] [char](5) NOT NULL,
	[PhoneNumber] [varchar](15) NOT NULL,
	[EmailAddress] [varchar](50) NOT NULL,
	[Title] [varchar](50) NOT NULL,
	[CreatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [CreatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    [UpdatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [UpdatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT [XPKConsultant] PRIMARY KEY CLUSTERED ([ConsultantID] ASC),
 CONSTRAINT [XFK1Consultant] FOREIGN KEY ([LoginID]) REFERENCES [dbo].[Login]([LoginID]) ON DELETE CASCADE,
 CONSTRAINT [XAK1Consultant] UNIQUE NONCLUSTERED ([FirstName], [LastName]),
 CONSTRAINT [XAK2Consultant] UNIQUE NONCLUSTERED ([LoginID])
)
GO

CREATE TABLE [dbo].[ProjectConsultant](
	[ProjectConsultantID] [smallint] IDENTITY(1,1) NOT NULL,
	[ProjectID] [smallint] NOT NULL,
	[ConsultantID] [smallint] NOT NULL,
	[BillingRate] [decimal](10,2) NOT NULL,  
	[CreatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [CreatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    [UpdatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [UpdatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT [XPKProjectConsultant] PRIMARY KEY CLUSTERED ([ProjectConsultantID] ASC),
 CONSTRAINT [XFK1ProjectConsultant] FOREIGN KEY ([ProjectID]) REFERENCES [dbo].[Project]([ProjectID]) ON DELETE CASCADE,
 CONSTRAINT [XFK2ProjectConsultant] FOREIGN KEY ([ConsultantID]) REFERENCES [dbo].[Consultant]([ConsultantID]) ON DELETE CASCADE,
 CONSTRAINT [XAK1ProjectConsultant] UNIQUE NONCLUSTERED ([ProjectID], [ConsultantID])
)
GO

CREATE TABLE [dbo].[ProjectDetail](
	[ProjectDetailID] [smallint] IDENTITY(1,1) NOT NULL,
	[ProjectConsultantID] [smallint] NOT NULL,
	[WorkDate] [date] NOT NULL,  
	[WorkDescription] [varchar](255) NOT NULL,
	[WorkedHours] [decimal](10,2) NOT NULL,
	[CreatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [CreatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    [UpdatedBy] VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,
    [UpdatedDate] SMALLDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT [XPKProjectDetail] PRIMARY KEY CLUSTERED ([ProjectDetailID] ASC),
 CONSTRAINT [XFK1ProjectDetail] FOREIGN KEY ([ProjectConsultantID]) REFERENCES [dbo].[ProjectConsultant]([ProjectConsultantID]) ON DELETE CASCADE,
 CONSTRAINT [XAK1ProjectDetail] UNIQUE NONCLUSTERED ([ProjectConsultantID], [WorkDate])
)
GO