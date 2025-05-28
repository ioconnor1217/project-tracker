USE [project-tracker-db]
GO

CREATE TRIGGER trg_Update_Client
ON [dbo].[Client]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE [dbo].[Client]
    SET UpdatedBy = SYSTEM_USER,
        UpdatedDate = CURRENT_TIMESTAMP
    FROM [dbo].[Client] c
    INNER JOIN inserted i ON i.ClientID = c.ClientID;
END;
GO

CREATE TRIGGER trg_Update_Project
ON [dbo].[Project]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE [dbo].[Project]
    SET UpdatedBy = SYSTEM_USER,
        UpdatedDate = CURRENT_TIMESTAMP
    FROM [dbo].[Project] p
    INNER JOIN inserted i ON i.ProjectID = p.ProjectID;
END;
GO

CREATE TRIGGER trg_Update_Login
ON [dbo].[Login]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE [dbo].[Login]
    SET UpdatedBy = SYSTEM_USER,
        UpdatedDate = CURRENT_TIMESTAMP
    FROM [dbo].[Login] l
    INNER JOIN inserted i ON i.LoginID = l.LoginID;
END;
GO

CREATE TRIGGER trg_Update_Consultant
ON [dbo].[Consultant]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE [dbo].[Consultant]
    SET UpdatedBy = SYSTEM_USER,
        UpdatedDate = CURRENT_TIMESTAMP
    FROM [dbo].[Consultant] c
    INNER JOIN inserted i ON i.ConsultantID = c.ConsultantID;
END;
GO

CREATE TRIGGER trg_Update_ProjectConsultant
ON [dbo].[ProjectConsultant]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE [dbo].[ProjectConsultant]
    SET UpdatedBy = SYSTEM_USER,
        UpdatedDate = CURRENT_TIMESTAMP
    FROM [dbo].[ProjectConsultant] pc
    INNER JOIN inserted i ON i.ProjectConsultantID = pc.ProjectConsultantID;
END;
GO

CREATE TRIGGER trg_Update_ProjectDetail
ON [dbo].[ProjectDetail]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE [dbo].[ProjectDetail]
    SET UpdatedBy = SYSTEM_USER,
        UpdatedDate = CURRENT_TIMESTAMP
    FROM [dbo].[ProjectDetail] pd
    INNER JOIN inserted i ON i.ProjectDetailID = pd.ProjectDetailID;
END;
GO