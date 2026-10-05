CREATE DATABASE citas ;
USE citas ;

CREATE TABLE `Consultorios` (
  `ConNumero` int(3) NOT NULL,
  `ConNombre` varchar(50) NOT NULL,
  PRIMARY KEY (`ConNumero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Medicos` (
  `MedIdentificacion` char(10) NOT NULL,
  `MedNombres` varchar(50) NOT NULL,
  `MedApellidos` varchar(50) NOT NULL,
  PRIMARY KEY (`MedIdentificacion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Pacientes` (
  `PacIdentificacion` char(10) NOT NULL,
  `PacNombres` varchar(50) NOT NULL,
  `PacApellidos` varchar(50) DEFAULT NULL,
  `PacFechaNacimiento` date NOT NULL,
  `PacSexo` enum('M','F') NOT NULL,
  PRIMARY KEY (`PacIdentificacion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Tratamientos` (
  `TraNumero` int(11) NOT NULL AUTO_INCREMENT,
  `TraFechaAsignado` date NOT NULL,
  `TraDescripcion` text NOT NULL,
  `TraFechaInicio` date NOT NULL,
  `TraFechaFin` date NOT NULL,
  `TraObservaciones` text NOT NULL,
  `TraPaciente` char(10) NOT NULL,
  PRIMARY KEY (`TraNumero`),
  KEY `TraPaciente` (`TraPaciente`),
  CONSTRAINT `Tratamientos_ibfk_1` FOREIGN KEY (`TraPaciente`) REFERENCES `Pacientes` (`PacIdentificacion`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

CREATE TABLE `citas` (
  `CitNumero` int(11) NOT NULL AUTO_INCREMENT,
  `CitFecha` date NOT NULL,
  `CitHora` varchar(10) NOT NULL,
  `CitPaciente` char(10) NOT NULL,
  `CitMedico` char(10) NOT NULL,
  `CitConsultorio` int(3) NOT NULL,
  `CitEstado` enum('Asignada','Cumplida','Solicitada','Cancelada') NOT NULL DEFAULT 'Asignada',
  PRIMARY KEY (`CitNumero`),
  KEY `CitPaciente` (`CitPaciente`),
  KEY `CitMedico` (`CitMedico`),
  KEY `CitConsultorio` (`CitConsultorio`),
  CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`CitPaciente`) REFERENCES `Pacientes` (`PacIdentificacion`),
  CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`CitMedico`) REFERENCES `Medicos` (`MedIdentificacion`),
  CONSTRAINT `citas_ibfk_3` FOREIGN KEY (`CitConsultorio`) REFERENCES `Consultorios` (`ConNumero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
