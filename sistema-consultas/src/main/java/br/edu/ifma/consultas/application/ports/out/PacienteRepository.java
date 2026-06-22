package br.edu.ifma.consultas.application.ports.out;

import java.util.List;

import br.edu.ifma.consultas.domain.Paciente;

public interface PacienteRepository {
    void salvar(Paciente paciente);
    Paciente buscarPorId(Long id);
    List<Paciente> buscarTodos();
    
}
