import styled from 'styled-components';
import { neutral, darkPurple, lightYellow, darkYellow, lightGreen } from '../../constants/colors';

export const Container = styled.div`
  padding: 20px;
  background-color: ${neutral};
  min-height: 100vh;
  position: relative;
  overflow: hidden;
`;

export const TopRightBlob = styled.img`
  position: absolute;
  top: -18px;
  right: -32px;
  width: clamp(150px, 8vw, 180px);
  height: auto;
  z-index: 0;
  pointer-events: none;
  user-select: none;
  opacity: 0.7;
`;

export const BottomLeftBlob = styled.img`
  position: absolute;
  bottom: -18px;
  left: -32px;
  width: clamp(150px, 8vw, 180px);
  height: auto;
  z-index: 0;
  pointer-events: none;
  user-select: none;
  opacity: 0.7;
`;

export const Header = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
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
  margin-bottom: 32px;
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

export const MenuTitle = styled.h1`
  font-size: 20px;
  font-weight: 700;
  color: ${darkPurple};
  margin: 0 0 4px 0;
  z-index: 10;
  position: relative;
`;

export const MenuSubtitle = styled.p`
  font-size: 14px;
  font-weight: 400;
  color: ${darkPurple};
  margin: 0 0 24px 0;
  z-index: 10;
  position: relative;
`;

export const CardsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  z-index: 10;
  position: relative;

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;
