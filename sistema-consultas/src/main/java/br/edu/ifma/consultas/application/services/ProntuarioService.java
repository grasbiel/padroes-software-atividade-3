package br.edu.ifma.consultas.application.services;

import br.edu.ifma.consultas.application.ports.in.RegistrarProntuarioUseCase;
import br.edu.ifma.consultas.application.ports.out.ConsultaRepository;
import br.edu.ifma.consultas.application.ports.out.ProntuarioRepository;
import br.edu.ifma.consultas.domain.Consulta;
import br.edu.ifma.consultas.domain.Prontuario;

public class ProntuarioService implements RegistrarProntuarioUseCase{
    
    // Portas de saída para o serviço buscar e salvar os dados
    private final ProntuarioRepository prontuarioRepository;
    private final ConsultaRepository consultaRepository;


    // Construtor
    public ProntuarioService(ProntuarioRepository prontuarioRepository, ConsultaRepository consultaRepository){
        this.prontuarioRepository = prontuarioRepository;
        this.consultaRepository = consultaRepository;
    }

    @Override
    public void registrarNovoProntuario(Prontuario prontuario, Long idConsulta){
        Consulta consulta = consultaRepository.buscarPorId(idConsulta);
       
        if (consulta == null) {
            throw new IllegalArgumentException("Consulta não encontrada no sistema");

        }

        prontuarioRepository.salvar(prontuario);
    }

}
