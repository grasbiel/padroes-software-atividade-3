package br.edu.ifma.consultas.infrastructure.ports.out;


import br.edu.ifma.consultas.application.ports.out.ProntuarioRepository;
import br.edu.ifma.consultas.domain.Prontuario;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

public class ProntuarioRepositoryMock implements ProntuarioRepository {

    private static final Logger logger = Logger.getLogger(ProntuarioRepositoryMock.class.getName());
    private final List<Prontuario> bancoDadosMemoria = new ArrayList<>();

    @Override
    public void salvar(Prontuario prontuario){
        bancoDadosMemoria.add(prontuario);
        logger.info("Prontuário Salvo em Memória! ID: " + prontuario.getIdProntuario());
    }

    @Override
    public Prontuario buscarPorId(Long id){
        return bancoDadosMemoria.stream()
                .filter(p -> p.getIdProntuario().equals(id))
                .findFirst()
                .orElse(null);
    }

    @Override
    public Prontuario buscarPorConsultaId(Long idConsulta){
        return  bancoDadosMemoria.stream()
                .filter(p -> p.getConsulta().getIdConsulta().equals(idConsulta))
                .findFirst()
                .orElse(null);
    }
}

