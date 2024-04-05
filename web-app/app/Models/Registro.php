<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Registro extends Model
{
    protected $fillable = [
        'qtd_clusters',
        'normalizar_dados',
        'file_name',
        'response',
    ];

    protected $casts = [
        'response' => 'json',
    ];
}
