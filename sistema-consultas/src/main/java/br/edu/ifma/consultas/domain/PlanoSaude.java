package br.edu.ifma.consultas.domain;

public class PlanoSaude {

    private Long id;
    private String nome;

    // Construtor
    public PlanoSaude(Long id, String nome){
        this.id = id;
        this.nome = nome;
    }

    public Long getId() {
        return id;
    }

    public String getNome() {
        return nome;
    }
}
