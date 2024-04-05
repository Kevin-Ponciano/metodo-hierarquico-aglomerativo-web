<?php

namespace App\Livewire;

use App\Models\Registro;
use Illuminate\Support\Arr;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;
use Livewire\Attributes\On;
use Livewire\Component;
use Livewire\WithFileUploads;
use Livewire\WithPagination;

class App extends Component
{
    use WithFileUploads;
    use WithPagination;

    public $file;
    public $qtdClusters=1;
    public $normalizarDados;
    public $url = 'http://n8n:5678/webhook/34dfbc5f-04c1-4881-8d39-7d344130eada';
    public $registro;

    public function mount(){

    }

    public function render()
    {
        return view('livewire.app', [
            'registros' => Registro::orderBy('id','desc')->paginate(10)
        ]);
    }

    public function save()
    {
        $path = $this->file->storeAs(path: 'files', name: $this->file->getClientOriginalName());
        $response = $this->sendWebhook(Storage::get($path), $path);
        if ($response->successful()) {
            $this->dispatch('success', 'Arquivo enviado com sucesso!');
            $newRegistro = Registro::create([
                'qtd_clusters' => $this->qtdClusters,
                'normalizar_dados' => $this->normalizarDados ? 'True' : 'False',
                'file_name' => $this->file->getClientOriginalName(),
                'response' => $response->json(),
            ]);

            $this->registro = $newRegistro;
            $this->dispatch('fileUploaded');
            $this->dispatch('view');
        } else {
            $this->dispatch('error', 'Erro ao enviar arquivo!');
            debug($response->json());
        }

        Storage::delete($path);
    }

    public function sendWebhook($file, $path)
    {
        return Http::withOptions([
            'verify' => false,
        ])
            ->attach('data', $file, $path)
            ->post($this->url, [
                'qtdClusters' => $this->qtdClusters,
                'normalizarDados' => $this->normalizarDados ? 'True' : 'False',
                'fileName' => $path,
            ]);
    }

    //#[on('view')]
    public function view($id)
    {
        $this->registro = Registro::find($id)->toArray();
        debug($this->registro['response']['response']['Cluster - 1']['atributos'][0]);
        //$this->dispatch('openModal');
    }
}
