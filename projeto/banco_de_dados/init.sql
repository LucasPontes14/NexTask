CREATE DATABASE IF NOT EXISTS db_tarefas;
USE db_tarefas;

CREATE TABLE IF NOT EXISTS usuario(
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_usuario)
);

CREATE TABLE IF NOT EXISTS lista(
    id_lista INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_lista),
    FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tarefa(
    id_tarefa INT NOT NULL AUTO_INCREMENT,
    id_lista INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    prioridade ENUM('baixa', 'media', 'alta') NOT NULL DEFAULT 'media',
    status ENUM('pendente', 'em andamento', 'concluida') NOT NULL DEFAULT 'pendente',
    data_venc DATE,
    hora_venc TIME,
    criado_em DATETIME NOT NULL
     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tarefa),
    FOREIGN KEY (id_lista) REFERENCES lista(id_lista)
    ON DELETE CASCADE
);