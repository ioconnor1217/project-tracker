INSERT INTO [dbo].[Client]
           ([Company],
           [Street],
           [City],
           [State],
           [PostalCode],
           [Phone],
           [Email])
VALUES
           ('Wu Tang Financial',
           '36 Shoalin St',
           'New York',
           'NY',
           '10001',
           '212-555-1234',
           'cappa@wufinance.com')
GO

INSERT INTO [dbo].[Project]
			([ProjectName])
VALUES 
			('Corporate Restructuring'),
			('Financial Analysis'),
			('Risk Assessment');

GO

INSERT INTO [dbo].[Consultant]
			([FName],
			[LName],
			[City],
			[State],
			[PostalCode],
			[Phone],
			[Email],
			[Role],
			[Rate])
VALUES 
			('Ghostface',
			'Killah',
			'New York',
			'NY',
			'10001',
			'212-555-5678',
			'ghost@wufinance.com',
			'Senior Analyst',
			200.00),

			('Chef',
			'Raekwon',
			'Newark',
			'NJ',
			'07102',
			'973-555-4321',
			'rae@wufinance.com',
			'Risk Consultant',
			180.00),

			('Ol','Dirty',
			'Brooklyn',
			'NY',
			'11201',
			'718-555-9090',
			'bigbabyjesus@wufinance.com',
			'Financial Advisor',
			190.00);

GO

INSERT INTO [dbo].[ProjectConsultant]
			([ProjectID],
			[ConsultantID],
			[BillingRate])
VALUES 
			(1, 1, 210.00),  -- Ghostface assigned to Corporate Restructuring
			(1, 2, 190.00),  -- Raekwon assigned to Corporate Restructuring
			(2, 3, 200.00),  -- ODB assigned to Financial Analysis
			(3, 2, 180.00);  -- Raekwon assigned to Risk Assessment
GO

INSERT INTO [dbo].[ProjectDetail]
			([ProjectConsultantID],[ClientID], [WorkDate], [WorkDescription], [WorkedHours])
VALUES 
			(1, 1, '2025-03-15', 'Developed financial restructuring strategy', 5.5),
			(2, 1, '2025-03-16', 'Analyzed corporate risk factors', 4.0),
			(3, 1, '2025-03-17', 'Reviewed investment portfolio', 6.0),
			(4, 1, '2025-03-18', 'Identified key risk areas in market trends', 3.5);
GO