package br.edu.ifma.consultas.application.ports.out;

import java.time.LocalDate;
import java.util.List;

import br.edu.ifma.consultas.domain.Consulta;

public interface ConsultaRepository {
    void salvar(Consulta consulta);
    Consulta buscarPorId(Long id);
    List<Consulta> buscarConsultasDoDia(LocalDate data);
}
