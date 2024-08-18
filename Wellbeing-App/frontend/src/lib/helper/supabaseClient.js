import { createClient } from "@supabase/supabase-js";

const supabaseUrl = 'https://aherzeuuccxtaqlrglfo.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFoZXJ6ZXV1Y2N4dGFxbHJnbGZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTcyOTEsImV4cCI6MjAzMTg3MzI5MX0.dEKDAiN-RNZ6ACBTGXH7VXOmv2dQ-lAjuJS2JFpUwVE';

export const supabase = createClient(supabaseUrl, supabaseKey);