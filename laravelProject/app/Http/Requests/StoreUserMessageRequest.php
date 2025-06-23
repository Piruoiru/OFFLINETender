<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreUserMessageRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // aggiungi policy se vuoi limitare per user
    }

    public function rules(): array
    {
        return [
            'content' => 'required|string|max:4000',
        ];
    }
}