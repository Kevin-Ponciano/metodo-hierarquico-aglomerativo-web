<?php

namespace App\Livewire;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Livewire\Component;

class App extends Component
{
    public function render()
    {
        return view('livewire.app');
    }

    public function upload(Request $request)
    {
        $url = 'https://webhook.n8n.laravix.com.br/webhook/284a51c5-dba2-476b-affe-524767e1454e';

        # send post with file
        $response = Http::withOptions([
            'verify' => false,
        ])
            ->withHeaders([
                'Accept' => 'application/json',
                'Content-Type' => 'multipart/form-data',
            ])
            ->attach('file', $request->file('file'))
            ->post($url);

        dd($response->json());
    }
}
