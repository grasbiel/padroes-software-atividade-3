package br.edu.ifma.consultas.domain;

public class Medicamento {

    private Long idMedicamento;
    private String nomeMedicamento;

    public Medicamento(Long idMedicamento, String nomeMedicamento){
        this.idMedicamento = idMedicamento;
        this.nomeMedicamento = nomeMedicamento;
    }

    public Long getIdMedicamento() {
        return idMedicamento;
    }

    public String getNomeMedicamento() {
        return nomeMedicamento;
    }
}
