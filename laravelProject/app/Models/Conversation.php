<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Conversation extends Model
{
    protected $fillable = [
        'title', // o altri campi che hai nella tua tabella
        'active', // Indica se la conversazione è attiva o meno
    ];

    /**
     * Relazione con i messaggi (una conversazione ha molti messaggi)
     */
    public function messages(): HasMany
    {
        return $this->hasMany(Message::class);
    }
}
