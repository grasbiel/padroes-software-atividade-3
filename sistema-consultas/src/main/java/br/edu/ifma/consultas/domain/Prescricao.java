package br.edu.ifma.consultas.domain;

public class Prescricao {

    private Long idPrescricao;
    private Medicamento medicamento;
    private String dosagem;
    private String administracao;
    private String tempoDeUso;

    public Prescricao(String administracao, String dosagem, Long idPrescricao, Medicamento medicamento, String tempoDeUso) {
        this.administracao = administracao;
        this.dosagem = dosagem;
        this.idPrescricao = idPrescricao;
        this.medicamento = medicamento;
        this.tempoDeUso = tempoDeUso;
    }

    public String getAdministracao() {
        return administracao;
    }

    public String getDosagem() {
        return dosagem;
    }

    public Long getIdPrescricao() {
        return idPrescricao;
    }

    public Medicamento getMedicamento() {
        return medicamento;
    }

    public String getTempoDeUso() {
        return tempoDeUso;
    }
}
