IF DB_ID(N'DatosAbiertosDB') IS NULL
    CREATE DATABASE DatosAbiertosDB;
GO
USE DatosAbiertosDB;
GO
IF OBJECT_ID(N'dbo.RegistrosAPI', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.RegistrosAPI (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_api VARCHAR(64) NOT NULL UNIQUE,
        titulo NVARCHAR(500) NULL,
        descripcion NVARCHAR(500) NULL,
        idioma NVARCHAR(500) NULL,
        medio NVARCHAR(500) NULL,
        formato NVARCHAR(500) NULL,
        disponible NVARCHAR(500) NULL,
        publicada NVARCHAR(500) NULL,
        json_original NVARCHAR(MAX) NOT NULL,
        fecha_captura DATETIME2 NOT NULL DEFAULT SYSDATETIME()
    );
END;
GO
SELECT COUNT(*) AS registros_actuales FROM dbo.RegistrosAPI;
GO
