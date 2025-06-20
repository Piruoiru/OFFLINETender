<?php

use App\Models\Conversation;
use Illuminate\Support\Facades\Broadcast;

Broadcast::channel('conversations.{conversation}', function ($user, Conversation $conversation) {
    // autorizza se l’utente appartiene alla conversazione
    return $conversation->users->contains($user);
});