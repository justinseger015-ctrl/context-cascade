import { useState, useEffect } from 'react';

export interface Skill {
  name: string;
  path: string;
  category?: string;
}

/**
 * Hook to fetch available skills from the backend
 * In production, this will call the API endpoint that lists .claude/skills
 *
 * For now, returns mock data until backend endpoint is implemented
 */
export function useSkills() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        setLoading(true);
        setError(null);

        // TODO: Replace with actual API call when backend endpoint is ready
        // const response = await fetch('/api/v1/skills');
        // const data = await response.json();
        // setSkills(data);

        // Mock data for development
        const mockSkills: Skill[] = [
          { name: 'agent-creator', path: 'agent-creator', category: 'Creation' },
          { name: 'code-review-assistant', path: 'code-review-assistant', category: 'Quality' },
          { name: 'feature-dev-complete', path: 'feature-dev-complete', category: 'Development' },
          { name: 'functionality-audit', path: 'functionality-audit', category: 'Quality' },
          { name: 'github-code-review', path: 'github-code-review', category: 'GitHub' },
          { name: 'hooks-automation', path: 'hooks-automation', category: 'Automation' },
          { name: 'pair-programming', path: 'pair-programming', category: 'Development' },
          { name: 'python-specialist', path: 'language-specialists/python-specialist', category: 'Languages' },
          { name: 'react-specialist', path: 'frontend-specialists/react-specialist', category: 'Frontend' },
          { name: 'testing-quality', path: 'testing-quality', category: 'Testing' },
          { name: 'typescript-specialist', path: 'language-specialists/typescript-specialist', category: 'Languages' },
        ];

        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 300));

        setSkills(mockSkills);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch skills');
      } finally {
        setLoading(false);
      }
    };

    fetchSkills();
  }, []);

  return { skills, loading, error };
}

/**
 * Group skills by category
 */
export function groupSkillsByCategory(skills: Skill[]): Record<string, Skill[]> {
  return skills.reduce((acc, skill) => {
    const category = skill.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(skill);
    return acc;
  }, {} as Record<string, Skill[]>);
}
