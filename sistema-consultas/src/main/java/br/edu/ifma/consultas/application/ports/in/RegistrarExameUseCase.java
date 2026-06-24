package br.edu.ifma.consultas.application.ports.in;

import br.edu.ifma.consultas.domain.Exame;

public interface RegistrarExameUseCase {

    void registrarNovoExame(Long idExame, Exame exame);
}
