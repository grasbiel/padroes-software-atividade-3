package br.edu.ifma.consultas.application.ports.out;

import java.util.List;

import br.edu.ifma.consultas.domain.Exame;

public interface ExameRepository {
    Exame buscarPorId(Long id);
    List<Exame> buscarPorTodos();
}
