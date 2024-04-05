<div class="container">
    <div class="card">
        <div class="table-responsive">
            <table class="table table-vcenter card-table">
                <thead>
                <tr>
                    <th>Agrupamentos</th>
                    <th>Clusters</th>
                    <th>Normalizado</th>
                    <th>Data e hora</th>
                    <th class="w-1"></th>
                </tr>
                </thead>
                <tbody>
                @foreach($registros as $item)
                    <tr>
                        <td>{{$item->file_name}}</td>
                        <td class="text-secondary">
                            {{$item->qtd_clusters}}
                        </td>
                        <td class="text-secondary">
                            {{$item->normalizar_dados === 'True' ? 'Sim' : 'Não'}}
                        </td>
                        <td class="text-secondary">
                            {{$item->created_at}}
                        </td>
                        <td>
                            <a href="#" data-bs-toggle="modal" data-bs-target="#modal-view"
                               wire:click="view({{$item->id}})">
                                Visualizar
                            </a>
                        </td>
                    </tr>
                @endforeach
                </tbody>
            </table>
            <div class="m-3">
                {{$registros->links()}}
            </div>
        </div>
    </div>
    <x-modal-create/>
    <x-modal-view :registro="$registro"/>
</div>

