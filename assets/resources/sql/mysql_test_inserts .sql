USE ProjectTracker;

-- Insert Client
INSERT INTO Client (`Company`, `Street`, `City`, `State`, `PostalCode`, `PhoneNumber`, `EmailAddress`)
VALUES
    ('Wu Tang Financial', '36 Shaolin St', 'New York', 'NY', '10001', '212-555-1234', 'cappa@wufinance.com');

-- Insert Projects
INSERT INTO Project (`ClientID`, `ProjectName`, `StartDate`)
VALUES 
    (1, 'Corporate Restructuring', CURDATE()),
    (1, 'Financial Analysis', CURDATE()),
    (1, 'Risk Assessment', CURDATE());

-- Insert Logins
INSERT INTO Login (`UserName`, `Password`)
VALUES 
    ('ghostface', 'shogun36'),
    ('chefraekwon', 'purpletape'),
    ('bigbabyjesus', 'dirtmcgirt');

-- Insert Consultants
INSERT INTO Consultant (`LoginID`, `FirstName`, `LastName`, `EmailAddress`, `PhoneNumber`)
VALUES 
    (1, 'Ghostface', 'Killah', 'ghost@wufinance.com', '212-555-5678'),
    (2, 'Chef', 'Raekwon', 'rae@wufinance.com', '973-555-4321'),
    (3, 'Ol', 'Dirty', 'bigbabyjesus@wufinance.com', '718-555-9090');

-- Insert ProjectConsultants (with assumed additional column BillingRate)
ALTER TABLE ProjectConsultant ADD COLUMN BillingRate DECIMAL(10,2);

INSERT INTO ProjectConsultant (`ProjectID`, `ConsultantID`, `BillingRate`)
VALUES 
    (1, 1, 210.00),  -- Ghostface
    (1, 2, 190.00),  -- Raekwon
    (2, 3, 200.00),  -- ODB
    (3, 2, 180.00);  -- Raekwon

-- Create ProjectDetail table with updated schema if needed
DROP TABLE IF EXISTS ProjectDetail;
CREATE TABLE ProjectDetail (
    DetailID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectID SMALLINT NOT NULL,
    ConsultantID SMALLINT NOT NULL,
    Task VARCHAR(100) NOT NULL,
    Hours DECIMAL(10,2) NOT NULL,
    WorkDate DATE NOT NULL,
    CreatedBy VARCHAR(50) NOT NULL DEFAULT CURRENT_USER(),
    CreatedDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedBy VARCHAR(50) NOT NULL DEFAULT CURRENT_USER(),
    UpdatedDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID),
    FOREIGN KEY (ConsultantID) REFERENCES Consultant(ConsultantID)
);

-- Insert ProjectDetails (adjusted to include ProjectID and ConsultantID directly)
INSERT INTO ProjectDetail (`ProjectID`, `ConsultantID`, `WorkDate`, `Task`, `Hours`)
VALUES 
    (1, 1, '2025-03-15', 'Developed financial restructuring strategy', 5.5),
    (1, 2, '2025-03-16', 'Analyzed corporate risk factors', 4.0),
    (2, 3, '2025-03-17', 'Reviewed investment portfolio', 6.0),
    (3, 2, '2025-03-18', 'Identified key risk areas in market trends', 3.5);