package br.edu.ifma.consultas.application.ports.out;

import br.edu.ifma.consultas.domain.Prontuario;

public interface ProntuarioRepository {
    void salvar(Prontuario prontuario);
    Prontuario buscarPorId(Long id);
    Prontuario buscarPorConsultaId(Long idConsulta);
}
