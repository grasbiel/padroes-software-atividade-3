package br.edu.ifma.consultas.domain;

import java.util.ArrayList;
import java.util.List;

public class Prontuario {

    private Long idProntuario;
    private Consulta consulta;
    private double peso;
    private double altura;
    private String descricaoSintomas;
    private String observacaoClinica;

    private List<Exame> exames;
    private ArrayList<Prescricao> prescricoes;

    public Prontuario(double altura, Consulta consulta, String descricaoSintomas, Long idProntuario, String observacaoClinica, double peso) {
        this.altura = altura;
        this.consulta = consulta;
        this.descricaoSintomas = descricaoSintomas;
        this.idProntuario = idProntuario;
        this.observacaoClinica = observacaoClinica;
        this.peso = peso;
        this.exames = new ArrayList<>();
        this.prescricoes = new ArrayList<>();
    }

    public void adicionarExame(Exame exame){
        this.exames.add(exame);
    }

    public void adicionarPrescricao(Prescricao prescricao){
        this.prescricoes.add(prescricao);
    }

    public ArrayList<Prescricao> getPrescricoes() {
        return prescricoes;
    }

    public double getPeso() {
        return peso;
    }

    public String getObservacaoClinica() {
        return observacaoClinica;
    }

    public Long getIdProntuario() {
        return idProntuario;
    }

    public List<Exame> getExames() {
        return exames;
    }

    public String getDescricaoSintomas() {
        return descricaoSintomas;
    }

    public Consulta getConsulta() {
        return consulta;
    }

    public double getAltura() {
        return altura;
    }
}
