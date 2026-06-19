package br.edu.ifma.consultas.domain;

public class Medico {

    private Long idMedico;
    private String nomeMedico;
    private String crm;

    public Medico(String crm, Long idMedico, String nomeMedico) {
        this.crm = crm;
        this.idMedico = idMedico;
        this.nomeMedico = nomeMedico;
    }

    public String getCrm() {
        return crm;
    }

    public Long getIdMedico() {
        return idMedico;
    }

    public String getNomeMedico() {
        return nomeMedico;
    }
}
