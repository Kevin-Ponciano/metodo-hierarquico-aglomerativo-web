<div class="modal modal-blur fade" wire:ignore.self id="modal-create" tabindex="-1" style="display: none;"
     aria-modal="true"
     role="dialog">
    <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Método Hierárquico Aglomerativo</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form wire:submit="save">
                <div class="modal-body">
                    <div class="row">
                        <div class="mb-3 col-6">
                            <label class="form-label">Quantidade de Clusters</label>
                            <input type="number" class="form-control" required data-ms-editor="true"
                                   wire:model="qtdClusters">
                        </div>
                        <div class="mb-3 col-6">
                            <label class="form-label">Normalizar Dados?</label>
                            <input type="checkbox" class="form-check-input" data-ms-editor="true"
                                   wire:model="normalizarDados">
                        </div>
                    </div>

                    <div class="row">
                        <label class="form-label">Arquivo</label>
                        <div class="col-auto">
                            <input type="file" accept="text/plain" class="form-control" required data-ms-editor="true"
                                   wire:model="file">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <a href="#" class="btn btn-link link-secondary" data-bs-dismiss="modal">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary ms-auto">
                        <!-- Download SVG icon from http://tabler-icons.io/i/plus -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                             stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                             stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                            <path d="M12 5l0 14"></path>
                            <path d="M5 12l14 0"></path>
                        </svg>
                        Calcular
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
@script
<script>
    $wire.on('fileUploaded', () => {
        $('#modal-create').modal('hide');
    })
</script>
@endscript
