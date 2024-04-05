<div class="modal modal-blur fade" id="modal-view" tabindex="-1" style="display: none;" aria-hidden="true">
    <div class="modal-dialog modal-full-width modal-dialog-centered" role="document">
        @if($registro)
            <div class="modal-content">
                <div class="modal-header">
                    <div class="d-flex">
                        <h5 class="modal-title">
                            {{$registro['file_name']}}
                        </h5>
                        @php
                            $colors = []; // Armazena as cores para garantir que sejam aplicadas consistentemente aos clusters durante uma única renderização.
                        @endphp
                        @foreach($registro['response']['response'] as $clusterName => $clusterDetails)
                            @php
                                // Gera uma cor aleatória se ainda não foi gerada para este cluster.
                                if (!array_key_exists($clusterName, $colors)) {
                                    $randomColor = sprintf('#%06X', mt_rand(0, 0xFFFFFF));
                                    $colors[$clusterName] = $randomColor;
                                }
                            @endphp
                            <div class="text-center mx-3">
                                <div>
                                    <div
                                        style="display: inline-block; width: 15px; height: 15px; background-color: {{ $colors[$clusterName] }}; margin-left: 10px; border: 1px solid #000;">

                                    </div>
                                    <span>{{$clusterName}}</span>
                                </div>
                                SSE - {{number_format($clusterDetails['SSE'], 2, '.', '')}}
                            </div>
                        @endforeach
                    </div>

                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="">
                    <div class="table-responsive">
                        <table class="table table-vcenter card-table">
                            <thead>
                            <tr>
                                <th>Cluster</th>
                                @foreach($this->registro['response']['response']['Cluster - 1']['atributos'][0] as $key => $elemento)
                                    <th>Atributo - {{$key + 1}}</th>
                                @endforeach
                            </tr>
                            </thead>
                            <tbody>
                            @foreach($registro['response']['response'] as $clusterName => $clusterDetails)
                                @foreach($clusterDetails['atributos'] as $atributoIndex => $atributo)
                                    <tr style="background-color: {{ $colors[$clusterName] }};">
                                        <td>
                                            {{$clusterName}}
                                        </td>
                                        @foreach($atributo as $elemento)
                                            <td>{{number_format($elemento, 2, '.', '')}}</td>
                                        @endforeach
                                    </tr>
                                @endforeach
                            @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn me-auto" data-bs-dismiss="modal">Fechar</button>
                </div>
            </div>
        @endif
    </div>
</div>
@script
<script>
    $wire.on('view', () => {
        $('#modal-view').modal('show');
    })
</script>
@endscript
