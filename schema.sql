USE [ProjectTracker]
GO

DROP TABLE IF EXISTS [dbo].[Client]
GO

CREATE TABLE [dbo].[Client](
	[ClientID] [smallint] IDENTITY(1,1) NOT NULL,
	[Company] [varchar](255) NOT NULL,  
	[Street] [varchar](50) NOT NULL,
	[City] [varchar](50) NOT NULL,
	[State] [char](2) NOT NULL,  
	[PostalCode] [char](5) NOT NULL,
	[Phone] [varchar](15) NOT NULL,
	[Email] [varchar](50) NOT NULL,
 CONSTRAINT [XPKClient] PRIMARY KEY CLUSTERED ([ClientID] ASC),
 CONSTRAINT [XAK1Client] UNIQUE NONCLUSTERED ([Company] ASC)
 )
GO

DROP TABLE IF EXISTS [dbo].[Project]
GO

CREATE TABLE [dbo].[Project](
	[ProjectID] [smallint] IDENTITY(1,1) NOT NULL,
	[ProjectName] [varchar](50) NOT NULL,  
 CONSTRAINT [XPKProject] PRIMARY KEY CLUSTERED ([ProjectID] ASC),
 CONSTRAINT [XAK1Project] UNIQUE NONCLUSTERED ([ProjectName] ASC)
 )
GO

DROP TABLE IF EXISTS [dbo].[Consultant]
GO

CREATE TABLE [dbo].[Consultant](
	[ConsultantID] [smallint] IDENTITY(1,1) NOT NULL,
	[FName] [varchar](255) NOT NULL,  
	[Lname] [varchar](50) NOT NULL,
	[City] [varchar](50) NOT NULL,
	[State] [char](2) NOT NULL,  
	[PostalCode] [char](5) NOT NULL,
	[Phone] [varchar](15) NOT NULL,
	[Email] [varchar](50) NOT NULL,
	[Role] [varchar](50) NOT NULL,
	[Rate] [decimal](10,2) NOT NULL,
 CONSTRAINT [XPKConsultant] PRIMARY KEY CLUSTERED ([ConsultantID] ASC),
 CONSTRAINT [XAK1Consultant] UNIQUE NONCLUSTERED ([FName], [LName]) 
)
GO

DROP TABLE IF EXISTS [dbo].[ProjectConsultant]
GO

CREATE TABLE [dbo].[ProjectConsultant](
	[ProjectConsultantID] [smallint] IDENTITY(1,1) NOT NULL,
	[ProjectID] [smallint] NOT NULL,
	[ConsultantID] [smallint] NOT NULL,
	[BillingRate] [decimal](10,2) NOT NULL,  
 CONSTRAINT [XPKProjectConsultant] PRIMARY KEY CLUSTERED ([ProjectConsultantID] ASC),
 CONSTRAINT [XFK1ProjectConsultant_Project] FOREIGN KEY ([ProjectID]) REFERENCES [dbo].[Project]([ProjectID]) ON DELETE CASCADE,
 CONSTRAINT [XFK2ProjectConsultant_Consultant] FOREIGN KEY ([ConsultantID]) REFERENCES [dbo].[Consultant]([ConsultantID]) ON DELETE CASCADE,
 CONSTRAINT [XAK1ProjectConsultant] UNIQUE NONCLUSTERED ([ProjectID], [ConsultantID])
)
GO

DROP TABLE IF EXISTS [dbo].[ProjectDetail]
GO

CREATE TABLE [dbo].[ProjectDetail](
	[ProjectDetailID] [smallint] IDENTITY(1,1) NOT NULL,
	[ProjectConsultantID] [smallint] NOT NULL,
	[ClientID] [smallint] NOT NULL,
	[WorkDate] [date] NOT NULL,  
	[WorkDescription] [varchar](255) NOT NULL,
	[WorkedHours] [decimal](10,2) NOT NULL,
 CONSTRAINT [XPKProjectDetail] PRIMARY KEY CLUSTERED ([ProjectDetailID] ASC),
 CONSTRAINT [XFK1ProjectDetail_ProjectConsultant] FOREIGN KEY ([ProjectConsultantID]) REFERENCES [dbo].[ProjectConsultant]([ProjectConsultantID]) ON DELETE CASCADE,
 CONSTRAINT [XFK2ProjectDetail_Client] FOREIGN KEY ([ClientID]) REFERENCES [dbo].[Client]([ClientID]) ON DELETE CASCADE,
 CONSTRAINT [XAK1ProjectDetail] UNIQUE NONCLUSTERED ([ProjectConsultantID], [WorkDate])
)

GO