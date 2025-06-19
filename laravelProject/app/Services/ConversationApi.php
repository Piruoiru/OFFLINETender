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
        return Http::timeout(120)->post(url('/api/conversations'), [
            'title' => $title,
            'user_id' => auth()->id(),
        ]);
    }

    public function mount()
    {
        return Http::timeout(120)->get(url('/api/conversations'));;
    }

    public function sendchat(int $conversationId, string $content, string $sender)
     {
        return Http::timeout(120)->post(
            url("/api/conversations/{$conversationId}/messages"),
            [
                'content' => $content,
                'sender'  => $sender,
                'user_id' => auth()->id(),
            ]
        );
    }

    public function refresh(int $conversationId)
    {   
        return Http::timeout(120)->get(
            url("/api/conversations/{$conversationId}/messages")
        );

    }

    public function analyze(){
        return Http::baseUrl(config('services.llm.url'))
                ->timeout(3600)
                ->post('/analyze')
                ->throw();
    }
}