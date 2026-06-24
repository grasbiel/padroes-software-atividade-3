package br.edu.ifma.consultas.application.services;

import br.edu.ifma.consultas.application.ports.in.RegistrarExameUseCase;
import br.edu.ifma.consultas.application.ports.out.ExameRepository;
import br.edu.ifma.consultas.domain.Exame;

public class ExameService implements RegistrarExameUseCase {

    // Portas de saída
    private final ExameRepository exameRepository;

    // Construtor
    public ExameService(ExameRepository exameRepository) {
        this.exameRepository = exameRepository;
    }

    @Override
    public void registrarNovoExame(Exame exame, Long idExame){
        Exame exame =
    }
}
