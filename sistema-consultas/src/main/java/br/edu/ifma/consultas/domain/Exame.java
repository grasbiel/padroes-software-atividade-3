package br.edu.ifma.consultas.domain;

public class Exame {

    private Long idExame;
    private String nomeExame;

    public Exame(Long idExame, String nomeExame){
        this.idExame = idExame;
        this.nomeExame = nomeExame;
    }

    public Long getIdExame() {
        return idExame;
    }

    public String getNomeExame() {
        return nomeExame;
    }
}
