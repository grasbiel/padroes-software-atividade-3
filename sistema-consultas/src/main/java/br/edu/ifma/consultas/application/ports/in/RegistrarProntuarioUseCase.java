package br.edu.ifma.consultas.application.ports.in;

import br.edu.ifma.consultas.domain.Prontuario;

public interface RegistrarProntuarioUseCase {

    // Comando que o controler vai chamar
    void registrarNovoProntuario(Prontuario prontuario, Long idConsulta);

}
