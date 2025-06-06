<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Message extends Model
{
    protected $fillable = ['conversation_id', 'sender', 'content'];

    /**
     * Il messaggio appartiene a una conversazione
     */
    public function conversation(): BelongsTo
    {
        return $this->belongsTo(Conversation::class);
    }

    /**
     * Il messaggio può appartenere a un utente (opzionale)
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
