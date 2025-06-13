<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class ConversationApi
{
    /**
     * Crea una nuova conversazione via API e
     * restituisce la Response dell’HTTP client.
     */
    public function create(string $title)
    {
        return Http::post(url('/api/conversations'), [
            'title' => $title,
        ]);
    }

    public function refresh(int $conversationId)
    {
        return Http::get(url("/api/conversations/{$conversationId}/messages"));
    }

    public function sendchat(int $conversationId, string $content, string $sender)
     {
        return Http::post(
            url("/api/conversations/{$conversationId}/messages"),
            [
                'content' => $content,
                'sender'  => $sender,
            ]
        );
    }
}