<?php

namespace App\Livewire;

use Livewire\Component;

class ChatAssistant extends Component
{
    public $conversations = [];
    public $activeConversation;
    public $messages = [];
    public $newMessage = '';

    public function mount()
    {
        $response = \Http::get(url('/api/conversations'));
        if ($response->successful()) {
            $this->conversations = $response->json();
        } else {
            $this->conversations = [];
        }
        // $this->conversations = [
        //     ['id' => 1, 'title' => 'Conversazione 1'],
        //     ['id' => 2, 'title' => 'Conversazione 2'],
        // ];
        //fare chiamata api che me le pesca da db laravel

        // $this->activeConversation = 1;
        // //metto come prima conversazione quella con id ultimo

        // $this->messages = [
        //     ['sender' => 'assistant', 'message' => 'Ciao! Come posso aiutarti?']
        // ];
        // Imposta la prima conversazione attiva (la più recente)
        // if (!empty($this->conversations)) {
        //     $this->activeConversation = collect($this->conversations)->last()['id'];
        //     $this->loadMessages($this->activeConversation);
        // }
        if (!empty($this->conversations)) {
            $this->activeConversation = collect($this->conversations)->last()['id'];
            $this->selectConversation($this->activeConversation);
        }
        // Carica i messaggi della conversazione attiva
        // $this->loadMessages($this->activeConversation);
    }

    public function selectConversation($id)
    {
        $this->activeConversation = $id;

        // Chiamata API per ottenere i messaggi
        $response = \Http::get(url("/api/conversations/{$id}/messages"));

        if ($response->successful()) {
            $this->messages = collect($response->json())->map(function ($msg) {
                return [
                    'sender' => $msg['sender'],
                    'message' => $msg['content'] ?? $msg['message'], // fallback per compatibilità
                ];
            })->toArray();
        } else {
            // Messaggi di errore fallback
            $this->messages = [
                ['sender' => 'system', 'message' => 'Impossibile caricare i messaggi.']
            ];
        }
    }

    public function sendMessage()
    {
        if (trim($this->newMessage) === '' || !$this->activeConversation) return;

        // Mostra subito il messaggio dell’utente
        $this->messages[] = [
            'sender' => 'user',
            'message' => $this->newMessage
        ];

        $userMessage = $this->newMessage;
        $this->newMessage = '';

        // Mostra messaggio "in elaborazione"
        $this->messages[] = [
            'sender' => 'assistant',
            'message' => 'Sto pensando...'
        ];

        try {
            $response = \Http::timeout(300)->post(url('/api/chat'), [
                'message' => $userMessage,
                'conversation_id' => $this->activeConversation,
            ]);

            if ($response->successful()) {
                $reply = $response->json()['reply'] ?? '[Nessuna risposta dal modello]';

                // Rimuovi "Sto pensando..." e metti risposta vera
                array_pop($this->messages); // rimuove ultimo (placeholder)
                $this->messages[] = [
                    'sender' => 'assistant',
                    'message' => $reply
                ];
            } else {
                array_pop($this->messages);
                $this->messages[] = [
                    'sender' => 'system',
                    'message' => 'Errore durante la comunicazione con il modello.'
                ];
            }
        } catch (\Exception $e) {
            array_pop($this->messages);
            $this->messages[] = [
                'sender' => 'system',
                'message' => 'Errore: ' . $e->getMessage()
            ];
        }
    }


    public function render()
    {
        return view('livewire.chat-assistant');
    }

    public function refreshMessages()
    {
        if (!$this->activeConversation) return;

        $response = \Http::get(url("/api/conversations/{$this->activeConversation}/messages"));

        if ($response->successful()) {
            $this->messages = collect($response->json())->map(function ($msg) {
                return [
                    'sender' => $msg['sender'],
                    'message' => $msg['content'] ?? $msg['message'],
                ];
            })->toArray();
        }
    }
}
