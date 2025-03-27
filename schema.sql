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
 CONSTRAINT [XPKClient] PRIMARY KEY CLUSTERED 
(
	[ClientID] ASC
),
 CONSTRAINT [XAK1Client] UNIQUE NONCLUSTERED 
(
	[Company] ASC
))
GO

--ALTER TABLE RELATIONSHIPS FK 


INSERT INTO [dbo].[Client]
           ([Company]
           ,[Street]
           ,[City]
           ,[State]
           ,[PostalCode]
           ,[Phone]
           ,[Email])
     VALUES
           (<Company, varchar(255),>
           ,<Street, varchar(50),>
           ,<City, varchar(50),>
           ,<State, char(2),>
           ,<PostalCode, char(5),>
           ,<Phone, varchar(15),>
           ,<Email, varchar(50),>)
GO

