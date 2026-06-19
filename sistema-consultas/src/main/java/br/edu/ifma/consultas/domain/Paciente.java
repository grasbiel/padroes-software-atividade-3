package br.edu.ifma.consultas.domain;

import java.time.LocalDate;

public class Paciente {
    // Atributos da classe
    private Long idPaciente;
    private String nomeCrianca;
    private String nomeResponsavel;
    private LocalDate dataNascimento;
    private String sexo;


    // Relacionamento com outras partes
    private Endereco endereco;
    private  PlanoSaude planoSaude;
    // Construtor
    public Paciente (Long idPaciente, String nomeCrianca, String nomeResponsavel, LocalDate dtNascimento, String sexo) {
        this.idPaciente = idPaciente;
        this.nomeCrianca = nomeCrianca;
        this.nomeResponsavel = nomeResponsavel;
        this.dataNascimento = dtNascimento;
        this.sexo = sexo;
    }

    public void vincularEndereco(Endereco endereco){
        this.endereco = endereco;
    }

    public void vincularPlanoSaude(PlanoSaude plano) {
        this.planoSaude = plano;
    }

    public Long getIdPaciente() {
        return idPaciente;
    }

    public String getNomeCrianca() {
        return nomeCrianca;
    }

    public String getNomeResponsavel() {
        return nomeResponsavel;
    }

    public LocalDate getDataNascimento() {
        return dataNascimento;
    }

    public String getSexo() {
        return sexo;
    }

    public Endereco getEndereco() {
        return endereco;
    }

    public PlanoSaude getPlanoSaude() {
        return planoSaude;
    }

}
