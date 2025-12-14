import styled from 'styled-components';
import { neutral, darkPurple, lightYellow, darkYellow, lightGreen } from '../../constants/colors';

export const Container = styled.div`
  padding: 20px;
  background: radial-gradient(120% 60% at 20% 10%, #eef2ff 0%, rgba(238, 242, 255, 0) 60%),
    radial-gradient(100% 40% at 80% 0%, #e0f7f1 0%, rgba(224, 247, 241, 0) 60%),
    ${neutral};
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
`;

export const Content = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
`;

export const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
`;

export const HelpButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: ${lightYellow};
  border: none;
  color: ${darkYellow};
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  &:active {
    transform: scale(0.95);
  }
`;

export const UserSection = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 10;
  position: relative;
`;

export const Avatar = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: ${lightGreen};
  flex-shrink: 0;
`;

export const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2px;
`;

export const Greeting = styled.p`
  font-size: 14px;
  font-weight: 400;
  color: ${darkPurple};
  margin: 0;
`;

export const UserName = styled.h2`
  font-size: 18px;
  font-weight: 700;
  color: ${darkPurple};
  margin: 0;
`;

export const HeroCard = styled.div`
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  margin-bottom: 20px;
`;

export const HeroTitle = styled.h1`
  font-size: 22px;
  font-weight: 800;
  color: ${darkPurple};
  margin: 0 0 6px 0;
`;

export const HeroSubtitle = styled.p`
  font-size: 14px;
  color: ${darkPurple};
  margin: 0 0 14px 0;
`;

export const ActionsRow = styled.div`
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
`;

export const PillAction = styled.button`
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid ${(p) => (p.$ghost ? '#e5e7eb' : darkPurple)};
  background: ${(p) => (p.$ghost ? '#f8fafc' : darkPurple)};
  color: ${(p) => (p.$ghost ? darkPurple : '#fff')};
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
  }
`;

export const SectionTitle = styled.h2`
  font-size: 18px;
  font-weight: 800;
  color: ${darkPurple};
  margin: 0 0 4px 0;
`;

export const MenuSubtitle = styled.p`
  font-size: 14px;
  font-weight: 400;
  color: ${darkPurple};
  margin: 0 0 18px 0;
`;

export const CardsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  z-index: 10;
  position: relative;

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;
