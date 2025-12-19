-- Add RLS policies for the users table
-- These policies control what users can do with their own data

-- Policy: Users can read their own user record
CREATE POLICY "Users can view own profile"
  ON public.users
  FOR SELECT
  USING (auth.uid() = id);

-- Policy: Users can update their own user record
CREATE POLICY "Users can update own profile"
  ON public.users
  FOR UPDATE
  USING (auth.uid() = id);

-- Note: INSERT is handled by the trigger with SECURITY DEFINER
-- We don't allow users to directly insert into users table
