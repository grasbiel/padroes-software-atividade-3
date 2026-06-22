package br.edu.ifma.consultas.application.ports.out;

import java.util.List;

import br.edu.ifma.consultas.domain.Medicamento;

public interface MedicamentoRepository {
    Medicamento buscarPorId(Long id);
    List<Medicamento> buscarTodos();
}
