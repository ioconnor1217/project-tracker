INSERT INTO [dbo].[Client]
           ([Company], [Street], [City], [State], [PostalCode], [PhoneNumber], [EmailAddress])
VALUES
           ('Wu Tang Financial', '36 Shaolin St', 'New York', 'NY', '10001', '212-555-1234', 'cappa@wufinance.com');
GO

INSERT INTO [dbo].[Project] ([Project])
VALUES 
    ('Corporate Restructuring'),
    ('Financial Analysis'),
    ('Risk Assessment');
GO

INSERT INTO [dbo].[Login] ([Login], [Password])
VALUES 
    ('ghostface', '$2b$12$XB6uvSESHcsmC3Mbo/1Tguh3Qp1T6p/.YP8myN1gST3H.8YzqnQWK'), --shogun36
    ('chefraekwon', '$2b$12$bvSeN61c5EuufW.TRlfRpeiJgei1XcW0CAsuwbPGdVDk.jYbGA0by'), --purpletape
    ('bigbabyjesus', '$2b$12$F6U2axOaSRkJQgQvEK35iuEgMRTvo.QNwlqDnqEmLMqsVJXmNus3W'); --dirtmcgirt
GO

INSERT INTO [dbo].[Consultant]
    ([LoginID], [FirstName], [LastName], [City], [State], [PostalCode], [PhoneNumber], [EmailAddress], [Title])
VALUES 
    (1, 'Ghostface', 'Killah', 'New York', 'NY', '10001', '212-555-5678', 'ghost@wufinance.com', 'Senior Analyst'),
    (2, 'Chef', 'Raekwon', 'Newark', 'NJ', '07102', '973-555-4321', 'rae@wufinance.com', 'Risk Consultant'),
    (3, 'Ol', 'Dirty', 'Brooklyn', 'NY', '11201', '718-555-9090', 'bigbabyjesus@wufinance.com', 'Financial Advisor');
GO

INSERT INTO [dbo].[ProjectConsultant] ([ProjectID], [ConsultantID], [BillingRate])
VALUES 
    (1, 1, 210.00),  -- Ghostface assigned to Corporate Restructuring
    (1, 2, 190.00),  -- Raekwon assigned to Corporate Restructuring
    (2, 3, 200.00),  -- ODB assigned to Financial Analysis
    (3, 2, 180.00);  -- Raekwon assigned to Risk Assessment
GO

INSERT INTO [dbo].[ProjectDetail] ([ProjectConsultantID], [ClientID], [WorkDate], [WorkDescription], [WorkedHours])
VALUES 
    (1, 1, '2025-03-15', 'Developed financial restructuring strategy', 5.5),
    (2, 1, '2025-03-16', 'Analyzed corporate risk factors', 4.0),
    (3, 1, '2025-03-17', 'Reviewed investment portfolio', 6.0),
    (4, 1, '2025-03-18', 'Identified key risk areas in market trends', 3.5);
GO