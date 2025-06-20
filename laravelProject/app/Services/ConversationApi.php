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

    public function askLLM(int $conversationId, string $prompt): string
    {
        $response = Http::baseUrl(config('services.llm.url'))
            ->timeout(3600)
            ->post('/chat', [
                'conversation_id' => $conversationId,
                'message'         => $prompt,
            ])
            ->throw();

        // restituisci solo la stringa con la risposta
        return $response->json('response', '');
    }

    public function sendChat(
        int $conversationId,
        string $content,
        string $sender,
        int $userId
    ): array {
        return Http::timeout(120)
            ->post(
                url("/api/conversations/{$conversationId}/messages"),
                [
                    'content' => $content,
                    'sender'  => $sender,
                    'user_id' => $userId,
                ]
            )
            ->throw()     // se status ≥ 400 il job finisce in failed()
            ->json();     // torna direttamente un array PHP
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