package br.edu.ifma.consultas.domain;

import java.time.LocalDateTime;

public class Consulta {

    private Long idConsulta;
    private Paciente paciente;
    private Medico medico;
    private LocalDateTime dataHora;
    private boolean novoPaciente;
    private boolean agendada;

    public Consulta(boolean agendada, LocalDateTime dataHora, Long idConsulta, Medico medico, boolean novoPaciente, Paciente paciente) {
        this.agendada = agendada;
        this.dataHora = dataHora;
        this.idConsulta = idConsulta;
        this.medico = medico;
        this.novoPaciente = novoPaciente;
        this.paciente = paciente;
    }

    public boolean isAgendada() {
        return agendada;
    }

    public LocalDateTime getDataHora() {
        return dataHora;
    }

    public Long getIdConsulta() {
        return idConsulta;
    }

    public Medico getMedico() {
        return medico;
    }

    public boolean isNovoPaciente() {
        return novoPaciente;
    }

    public Paciente getPaciente() {
        return paciente;
    }
}
